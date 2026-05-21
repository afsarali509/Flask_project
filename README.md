# Flask API + MongoDB Form App

A Flask application with:
- **`/api`** — returns a JSON list read from `data/items.json`
- **Form (`/`)** — inserts submissions into MongoDB Atlas; redirects to `/success` on success; shows errors on the same page on failure

## Setup

### 1. Create virtual environment and install dependencies

```powershell
cd "d:\project\python projects\per"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure MongoDB Atlas

1. Sign in at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a free cluster and a database user.
3. **Network Access** → Add IP Address → allow your IP (or `0.0.0.0/0` for development only).
4. **Database** → Connect → Drivers → copy the connection string.
5. Copy `.env.example` to `.env` and set your URI:

```powershell
copy .env.example .env
```

Edit `.env`:

```
MONGODB_URI=mongodb+srv://USER:PASSWORD@CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=flask_app
MONGODB_COLLECTION=submissions
```

Replace `USER`, `PASSWORD`, and `CLUSTER` with your Atlas values.

### 3. Run the application

```powershell
python app.py
```

Open http://127.0.0.1:5000 for the form.

## Testing

### Test `/api` (command)

```powershell
curl http://127.0.0.1:5000/api
```

**Expected response** (JSON list from `data/items.json`):

```json
[
  {"id": 1, "name": "Alice Johnson", "role": "Developer"},
  {"id": 2, "name": "Bob Smith", "role": "Designer"},
  {"id": 3, "name": "Carol Davis", "role": "Project Manager"}
]
```

Or in PowerShell:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api
```

### Test form submission

1. Go to http://127.0.0.1:5000
2. Fill Name, Email, Message → Submit
3. **Success:** redirect to http://127.0.0.1:5000/success with message *"Data submitted successfully"*
4. **Error:** e.g. wrong `MONGODB_URI` → error shown on the form page (no redirect)

Verify in Atlas: **Browse Collections** → `flask_app` → `submissions`.

## Project structure

```
per/
├── app.py              # Flask routes
├── data/
│   └── items.json      # Backend file for /api
├── templates/
│   ├── base.html
│   ├── index.html      # Form + error display
│   └── success.html    # Success message page
├── static/
│   └── style.css
├── requirements.txt
├── .env.example
└── README.md
```

## Submission document (Google Doc / Word)

Include the following in your submission doc:

| Section | What to attach |
|--------|----------------|
| **GitHub repo link** | URL after you push this project |
| **Screenshots** | (1) `/api` JSON in browser or terminal (2) Form filled (3) Success page (4) Optional: Atlas collection with inserted document (5) Optional: Error on form when DB fails |
| **Commands + explanation** | Copy setup/run/test commands from this README and briefly explain each step |

### Suggested doc outline

1. **Title & your name**
2. **GitHub repository link**
3. **Setup** — venv, `pip install`, `.env` for Atlas
4. **API route** — screenshot of `curl` or browser at `/api` + short explanation that data comes from `data/items.json`
5. **Form & MongoDB** — screenshots of form, success page, Atlas data
6. **Error handling** — screenshot showing error on same page (e.g. invalid URI) + explanation
7. **Conclusion** — what you learned

## Push to GitHub

```powershell
git init
git add .
git commit -m "Add Flask API and MongoDB form submission app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub details.
