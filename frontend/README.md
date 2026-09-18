# MultiDocumentRAG — Frontend

React + Vite chat UI for the MultiDocumentRAG FastAPI backend (`app.py`).
This is a presentation + API-client layer only — no retrieval, routing,
or model logic lives here. All of that stays in the Python backend.

## Setup

```bash
cd frontend
npm install
cp .env.example .env      # edit if your backend runs somewhere other than localhost:8000
npm run dev
```

The dev server runs at `http://localhost:5173`. Make sure the FastAPI
backend is running first:

```bash
# from the project root, one level up
uvicorn app:app --reload --port 8000
```

## Folder structure

```
src/
├── api/                  # The ONLY place that calls fetch() against the backend
│   ├── client.js          # base request wrapper, error normalization
│   ├── chat.js             # POST /api/chat, GET /api/health
│   ├── documents.js        # GET/POST/DELETE /api/documents, /api/upload
│   └── types.js            # JSDoc shapes matching app.py's Pydantic models
├── context/
│   └── ConversationContext.jsx   # provides chat state to the tree
├── hooks/
│   ├── useChat.js          # message list, send, regenerate, clear
│   └── useDocuments.js     # documents sidebar state (handles 501 gracefully)
├── components/
│   ├── layout/             # Sidebar, MainPanel
│   ├── chat/                # MessageList, MessageBubble, ChatInput, etc.
│   ├── citations/           # CitationChip, CitationRow
│   ├── indicators/          # RouteModelBadge (driven entirely by backend data)
│   └── documents/           # DocumentList, DocumentRow, UploadButton
├── App.jsx
├── main.jsx
└── index.css
```

## How the API layer works

Every backend call goes through `src/api/client.js`. Nothing else in the
app calls `fetch` directly. The backend base URL comes from
`VITE_API_BASE_URL` (see `.env.example`) — no secrets live in the
frontend; `GEMINI_API_KEY` etc. stay server-side in the Python backend.

Response shape the frontend expects from `POST /api/chat` (matches
`app.py` exactly):

```json
{
  "answer": "...",
  "route": "local",
  "provider": "ollama",
  "model": "gemma3:4b",
  "citations": [
    { "id": 1, "type": "document", "source": "...", "page": 42, "score": 0.6052, "url": null }
  ]
}
```

## Current backend status this frontend targets

- `POST /api/chat` — fully wired up.
- `GET /api/health` — fully wired up, shown implicitly (errors surface if backend/Ollama is down).
- `GET /api/documents`, `POST /api/upload`, `DELETE /api/documents/{id}` — the
  backend currently returns `501 Not Implemented` for these. The sidebar
  reflects that honestly ("Document management isn't wired up yet")
  instead of showing a fake empty list or pretending an upload succeeded.
- There is no `/api/chat/regenerate` endpoint yet. The "Regenerate" button
  re-sends the last user message through `/api/chat` client-side — when a
  dedicated endpoint exists, only `useChat.js`'s `regenerate` function
  needs to change.
- `route: "general"` is not yet returned by the backend (router.py only
  emits `local`/`web`), but the UI (badges, colors) already handles it so
  no frontend change will be needed when it's added.
