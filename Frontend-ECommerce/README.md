# Frontend-ECommerce (React + Vite)

Simple React frontend aligned to the provided FastAPI backend.

## Prerequisites
- Node.js 18+

## Setup
```bash
cd Frontend-ECommerce
npm install
cp .env.example .env # then edit VITE_API_BASE_URL if needed
npm run dev
```

Open the printed URL (default `http://localhost:5173`). Ensure backend CORS `FRONTEND_API` includes this origin.

## Environment
- `VITE_API_BASE_URL` must point to your backend `http://localhost:8000/api/v1` (or deployed URL)

## Notes
- JWT is stored in localStorage and added as `Authorization: Bearer <token>` for authenticated routes.
- Admin pages require an admin token; backend will return 403 if unauthorized.
- Product update uses POST `/product/:id`.
- Cart endpoints require the path `user_id` that matches the decoded user id from the token.

