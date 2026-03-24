# Deliva Backend (Delivery App API)

A Django REST API for a delivery platform with roles for customers, restaurants, and couriers. Includes authentication, menus, orders, deliveries, and notifications.

## Features
- Custom user model with roles (admin, customer, courier, restaurant owner)
- Restaurant management and menus
- Cart, checkout, and order tracking
- Courier assignments and delivery tracking
- Notification templates and push notifications (in-app)
- Swagger/Redoc API documentation

## Tech Stack
- Django 5.2
- Django REST Framework
- drf-yasg (OpenAPI/Swagger)
- SQLite (dev) — configurable for Postgres

## Project Structure
- `apps/accounts` – auth, roles, profiles
- `apps/customers` – addresses, wallets, transactions
- `apps/restaurants` – restaurants, deliveries
- `apps/menu` – categories and items
- `apps/orders` – cart, orders, checkout
- `apps/couriers` – rider profiles, vehicles, assignments
- `apps/notifications` – templates and notifications
- `config` – settings, URLs, ASGI/WSGI

## Local Setup
1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Copy `.env.example` to `.env` and fill values.
4. Run migrations.
5. Start the server.

## Environment Variables
See `.env.example` for all required variables.

## API Docs
- Swagger: `/swagger/`
- Redoc: `/redoc/`

## Notes
- This project is configured for token authentication.
- For production, set `DEBUG=False` and configure Postgres, allowed hosts, and security settings.
