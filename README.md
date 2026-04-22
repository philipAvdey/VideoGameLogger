# VideoGameLogger

A full-stack game logging app with a React + Vite frontend and Flask backend. The app searches IGDB for games and lets users save titles to a diary with ratings and completion dates.

## Project Structure

- `requirements.txt` — Python dependencies for the backend
- `src/backend/` — Flask API server and IGDB integration
- `src/frontend/` — React + Vite frontend

## Prerequisites

- Node.js 18+ (for frontend)
- npm (or yarn/pnpm)
- Python 3.11+ (recommended)
- `virtualenv` / `venv`

## Backend Setup

1. Create and activate a Python virtual environment at the project root:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file inside `src/backend/` with your IGDB credentials:

   ```env
   IGDB_CLIENT_ID=your_igdb_client_id
   IGDB_CLIENT_SECRET=your_igdb_client_secret
   ```

4. Start the backend from the `src/backend/` directory:

   ```bash
   cd src/backend
   export FLASK_APP=app
   flask run
   ```

   The backend will run by default at `http://localhost:5000`.

## Frontend Setup

1. Change into the frontend directory:

   ```bash
   cd src/frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the frontend dev server:

   ```bash
   npm run dev
   ```

   Vite will usually start at `http://localhost:5173`.

## Running the App

1. Start the backend first (`src/backend` / Flask on port 5000).
2. Start the frontend second (`src/frontend` / Vite).
3. Open the frontend URL shown by Vite in your browser.

## Notes

- The frontend calls the backend at `http://localhost:5000`.
- The backend exposes IGDB search at `GET /api/igdb/search?query=<term>`.
- The backend expects `IGDB_CLIENT_ID` and `IGDB_CLIENT_SECRET` in `src/backend/.env`.

## Common Commands

### Backend

```bash
source venv/bin/activate
cd src/backend
export FLASK_APP=app
flask run
```

### Frontend

```bash
cd src/frontend
npm install
npm run dev
```

## Troubleshooting

- If the frontend cannot reach the backend, verify that Flask is running on port `5000` and that the backend URL in the frontend matches it.
- If IGDB requests fail, confirm your `.env` keys are correct and that `src/backend/` is the working directory when you run Flask.
