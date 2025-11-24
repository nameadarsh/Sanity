# Installation Instructions

## ✅ Dependencies Installed

### Frontend (Node.js)
All frontend dependencies have been installed via `npm install` in the `frontend/` directory.

### Backend (Python)
All backend dependencies are listed in `requirements.txt` and `backend/requirements.txt`.

---

## 📝 Update Your .env File

Add these lines to your existing `.env` file in the **project root**:

```env
# Your existing variables (keep these):
GROQ_API_KEY=my api key
FLASK_ENV=development
MODEL_DIR=backend/model/distilbert
FINE_TUNED_MODEL_PATH=backend/model/sanity_model.bin
PROCESSED_DATA_DIR=backend/data/processed
RAW_DATA_DIR=backend/data/raw
CONFIDENCE_THRESHOLD=0.70

# ADD THESE NEW VARIABLES:
FLASK_PORT=5000
VITE_API_URL=http://localhost:5000
```

**Complete .env file should look like:**

```env
GROQ_API_KEY=my api key

FLASK_ENV=development
FLASK_PORT=5000

MODEL_DIR=backend/model/distilbert
FINE_TUNED_MODEL_PATH=backend/model/sanity_model.bin
PROCESSED_DATA_DIR=backend/data/processed
RAW_DATA_DIR=backend/data/raw

CONFIDENCE_THRESHOLD=0.70

VITE_API_URL=http://localhost:5000
```

---

## 🔧 Install Backend Dependencies

Run this command from the project root:

```bash
pip install -r requirements.txt
```

Or if you prefer to install from the backend folder:

```bash
cd backend
pip install -r requirements.txt
```

**Note:** It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate

# Then install
pip install -r requirements.txt
```

---

## 📦 Requirements Files

1. **`requirements.txt`** (root) - Complete Python requirements for the entire project
2. **`backend/requirements.txt`** - Backend-specific requirements (same as root)
3. **`frontend/package.json`** - Frontend Node.js dependencies (already installed)

---

## 🚀 Next Steps

### Step 1: Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Backend Setup
```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Test the health endpoint:
- Open browser: `http://localhost:5000/health`
- Should return: `{"status": "healthy"}`

### Step 3: Start Frontend (in a new terminal)
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

### Step 4: Test the Application

1. **Open Frontend:** `http://localhost:3000`
2. **Test Text Input:**
   - Paste some news text
   - Click "Analyze News"
   - View prediction results

3. **Test PDF Upload:**
   - Switch to PDF tab
   - Upload a PDF file
   - View results

4. **Test URL:**
   - Switch to URL tab
   - Enter a news article URL
   - View results

5. **Test Chat:**
   - After getting a prediction, click "Ask Follow-up Questions"
   - Ask questions about the article
   - Test both direct and follow-up questions

---

## ✅ Verification Checklist

- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install` in frontend/)
- [ ] `.env` file updated with new variables
- [ ] Backend runs on `http://localhost:5000`
- [ ] Frontend runs on `http://localhost:3000`
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] Can submit text/PDF/URL for prediction
- [ ] Chat interface works

---

## 🐛 Troubleshooting

### Backend won't start
- Check if port 5000 is available
- Verify all dependencies installed: `pip list`
- Check `.env` file exists and has correct paths

### Frontend can't connect to backend
- Ensure backend is running
- Check `VITE_API_URL` in `.env` matches backend URL
- Check CORS settings in backend

### Model not found
- Ensure model files exist in `backend/model/distilbert/`
- If missing, run: `python backend/scripts/train_model.py`

---

## 📚 Additional Resources

- **Setup Guide:** `SETUP_GUIDE.md`
- **Frontend Docs:** `frontend/README.md`
- **Backend Docs:** `backend/docs/`

