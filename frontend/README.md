# WasteAI frontend

React 19 + Vite + Tailwind CSS 4 single-page app for the waste-segregation
project.

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build in dist/
npm run lint
```

## How it talks to the backend

All HTTP calls live in `src/services/`:

| File | Purpose |
|---|---|
| `api.js` | Shared axios client, error normalisation (`ApiError`) |
| `wasteService.js` | One function per backend endpoint |

In development the Vite proxy forwards `/api` and `/health` to
`http://127.0.0.1:8000` (override with `VITE_DEV_API_TARGET`). For production
builds set `VITE_API_BASE_URL` to the API's public URL. See `.env.example`.

## Pages

- `/predict` – upload or capture an image, classify it, send feedback
- `/guide` – waste category overview
- `/decomposition` – live decomposition profiles from the knowledge base
- `/analytics` – live dashboard from saved predictions
