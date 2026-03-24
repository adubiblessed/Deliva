# Deliva Architecture & Program Flow

## System Overview
Deliva is a multi‑role delivery platform API with three primary user types: customers, restaurant owners, and couriers. The system manages order lifecycle from creation through delivery tracking.

## Core Entities & Relationships

```
User (Custom AbstractUser)
├── ADMIN
├── USER (Customer)
├── COURIER (Rider)
└── RESTAURANT_OWNER

Customer
├── CustomerProfile (wallet, address)
├── Address (multiple, ManyToMany)
├── Cart (one per restaurant)
│   └── CartItem (menu items)
├── Order (multiple)
│   └── OrderItem (menu items with price snapshot)
├── Wallet
│   └── Transaction (credit/debit)
└── Notification (received)

Restaurant
├── Owner (OneToOne User)
├── MenuCategory (multiple)
│   └── MenuItem (multiple)
├── Cart (multiple from customers)
└── Order (multiple)

Delivery/Courier
├── RiderProfile (OneToOne User)
├── Vehicle (multiple)
├── DeliveryAssignment (OneToOne per Delivery)
└── Delivery
    ├── Order (OneToOne)
    └── DeliveryTracking (multiple GPS points)

Notification
├── NotificationTemplate (trigger event + content)
└── Notification (user + template + payload)
```

## Key Workflows

### 1) User Authentication & Roles
```
POST /auth/register/ → UserRegistrationView
  ↓
Create User with role (USER|COURIER|RESTAURANT_OWNER|ADMIN)
  ↓
Token generated on login: POST /auth/login/
  ↓
All subsequent requests include: Authorization: Token <key>
```

### 2) Restaurant Setup
```
User creates Account with role=RESTAURANT_OWNER
  ↓
POST /restaurants/ → RestaurantsApiView.post()
  ↓
Create Restaurant (owner=user)
  ↓
POST /menu/categories/ → MenuCategoryView.post()
  ↓
POST /menu/items/ → MenuItemsApiView.post()
  ↓
Restaurant visible: GET /restaurants/all/
```

### 3) Customer Ordering Flow
```
GET /restaurants/all/ → Browse restaurants
  ↓
GET /restaurants/<id>/menu/ → See restaurant menu & items
  ↓
POST /orders/cart/ → Create cart (customer + restaurant)
  ↓
POST /orders/cart/items/ → Add menu item to cart
  → CartItem created: subtotal = price × quantity
  → Cart.cal_total() updates cart total
  ↓
PUT /orders/cart/items/<id>/ → Update quantity
  ↓
DELETE /orders/cart/items/<id>/ → Remove item
  ↓
POST /orders/checkout/ → Convert cart to order
  → Order created with all items
  → Order.tracking_code generated (DLV-XXXXXXXX)
  → Cart items cleared
  ↓
Order status: PENDING → PREPARING → OUT_FOR_DELIVERY → DELIVERED
```

### 4) Payment Integration
```
POST /orders/checkout/ 
  → payment_method: 'CASH_ON_DELIVERY' | 'CREDIT_CARD'
  ↓
Payment record created:
  → Payment.status = PENDING
  → Payment.reference generated (PAY-XXXXXXXXXX)
  ↓
PATCH /orders/<id>/status/ → Update to PREPARING
  → Payment.status = COMPLETED (if payment processed)
```

### 5) Delivery Assignment & Tracking
```
Order status = OUT_FOR_DELIVERY
  ↓
POST /riders/assign/ → Create DeliveryAssignment
  → Rider must be available (is_available=True)
  ↓
DeliveryAssignment created
  → assigned_at = now
  → accepted_at = null (until rider accepts)
  ↓
PATCH /riders/deliveries/<id>/status/ → Update delivery status
  → PENDING → PICKED_UP → EN_ROUTE → DELIVERED
  ↓
POST /riders/deliveries/<id>/track/ → Get real‑time location
  → DeliveryTracking records (lat/lon history)
  ↓
Customer: GET /orders/<id>/track/ → Track delivery
```

### 6) Rider/Courier Operations
```
User creates Account with role=COURIER
  ↓
POST /riders/ → Register RiderProfile
  → vehicle_type, license_plate, rating
  ↓
POST /riders/vehicles/ → Add vehicle info
  ↓
GET /riders/<id>/deliveries/ → List assigned deliveries
  ↓
PATCH /riders/deliveries/<id>/status/ → Update delivery (pickup → delivery)
  ↓
POST /riders/ratings/<id>/ → Receive & store rating from customer
```

### 7) Notification Flow
```
POST /notification/template/ → Create NotificationTemplate
  → trigger_event: WELCOME, DELIVERY, PROMOTIONAL, RESET_PASSWORD
  → template contains placeholders: {{username}}, {{order_id}}, etc.
  ↓
POST /notification/push/ → Send notification
  → NotificationService.notification_contents()
  → Populate template with payload
  → Create Notification record (is_read=False)
  ↓
Customer receives notification (in‑app)
  → Status: PENDING → SUCCESS | FAILED
```

## API Endpoint Map

### Authentication
- `POST /auth/register/` – Register new user
- `POST /auth/login/` – Get auth token
- `POST /auth/logout/` – Revoke token
- `GET /auth/me/` – Current user profile

### Restaurants
- `GET /restaurants/` – Owner's restaurants (auth required)
- `POST /restaurants/` – Create restaurant (auth required)
- `GET /restaurants/all/` – All active restaurants (public)
- `GET /restaurants/<id>/` – Get restaurant detail (auth required)
- `PUT /restaurants/<id>/` – Update restaurant (auth required)
- `DELETE /restaurants/<id>/` – Delete restaurant (auth required)
- `GET /restaurants/<id>/menu/` – Restaurant menu (public)

### Menu
- `GET /menu/items/` – All menu items
- `POST /menu/items/` – Create menu item
- `GET /menu/items/<id>/` – Get item detail
- `PUT /menu/items/<id>/` – Update item
- `DELETE /menu/items/<id>/` – Delete item
- `GET /menu/categories/` – All categories
- `POST /menu/categories/` – Create category
- `GET /menu/categories/<id>/` – Category + items

### Orders & Cart
- `GET /orders/cart/` – Get current cart
- `POST /orders/cart/` – Create cart
- `POST /orders/cart/items/` – Add item to cart
- `PUT /orders/cart/items/<id>/` – Update quantity
- `DELETE /orders/cart/items/<id>/` – Remove from cart
- `POST /orders/checkout/` – Create order from cart
- `GET /orders/orders/` – List user orders
- `GET /orders/orders/<id>/` – Get order detail
- `PATCH /orders/orders/<id>/status/` – Update order status
- `GET /orders/orders/<id>/track/` – Track delivery

### Couriers/Riders
- `GET /riders/` – List riders
- `POST /riders/` – Register rider
- `GET /riders/<id>/` – Rider profile
- `POST /riders/assign/` – Assign delivery to rider
- `GET /riders/delivery-assignments/` – List assignments
- `POST /riders/vehicles/` – Add vehicle
- `GET /riders/vehicles/` – List vehicles
- `GET /riders/<id>/deliveries/` – Rider's deliveries
- `PATCH /riders/deliveries/<id>/status/` – Update delivery status
- `GET /riders/deliveries/<id>/track/` – Track delivery
- `POST /riders/ratings/<id>/` – Rate rider
- `GET /riders/ratings/<id>/` – Get rider rating

### Customers
- `POST /customers/<user_id>/address/` – Add address
- `GET /customers/<user_id>/address/` – List addresses

### Notifications
- `POST /notification/template/` – Create notification template
- `POST /notification/push/` – Send notification

## Data Flow: Complete Order Lifecycle

```
1. Customer Registration
   User → POST /auth/register/ → User created (role=USER)

2. Browse & Order
   User → GET /restaurants/all/ → View restaurants
        → GET /restaurants/<id>/menu/ → View menu
        → POST /orders/cart/ → Create cart
        → POST /orders/cart/items/ → Add items
        → POST /orders/checkout/ → Create order

3. Order Processing
   Order created → PENDING
   Restaurant notified → Status: PREPARING
   Notification sent → Template rendered with order details

4. Delivery Assignment
   Order → OUT_FOR_DELIVERY
   DeliveryAssignment → Rider assigned
   Rider accepts → accepted_at = now

5. Real‑Time Tracking
   Rider updates location → DeliveryTracking records created
   Customer polls → GET /orders/<id>/track/ → Get latest location

6. Delivery Complete
   Status → DELIVERED
   Rating submitted → Rider rating updated
   Transaction recorded (if wallet payment)

7. Notification Archive
   Notifications saved with is_read status
```

## Authentication & Permissions Flow

```
Request → TokenAuthentication
  ↓
Token validated from Authorization header
  ↓
User attached to request
  ↓
View checks permissions:
  - IsAuthenticated (default for most endpoints)
  - AllowAny (public: register, login, all restaurants)
  ↓
If denied → 401 Unauthorized or 403 Forbidden
```

## Database Schema Highlights

- **BaseModel**: All models inherit UUID PK, created_at, updated_at, deleted_at, is_active (soft delete support).
- **Custom User**: EMAIL as USERNAME_FIELD, role‑based access.
- **Unique Constraints**: 
  - Cart item unique per cart + menu_item
  - Payment reference unique
  - Transaction reference unique
  - Order tracking_code unique
- **Relationships**: OneToOne for restaurant owner, profile; ForeignKey for most others.

## Key Architectural Decisions

- **Token Auth**: Simple and stateless, suitable for REST + mobile clients.
- **Soft Deletes**: All models support soft delete via is_active + deleted_at.
- **UUID PKs**: Better for distributed systems; avoids ID collision.
- **Custom User Model**: Role‑based, no separate Profile table for auth.
- **Service Layer**: Notifications use NotificationService for template rendering.
- **API Versioning**: Via URL structure (not yet implemented).


