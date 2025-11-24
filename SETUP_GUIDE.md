# Sanity Web App - Complete Setup Guide

## 📋 Prerequisites

- **Python 3.9+** (for backend)
- **Node.js 18+** and **npm** (for frontend)
- **Groq API Key** (for LLM verification)

---

## 🔧 Installation Steps

### 1. Backend Setup

```bash
# Navigate to project root
cd Sanity_V1

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Or install from backend folder
pip install -r backend/requirements.txt
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### 3. Environment Configuration

Create or update `.env` file in the **project root** with the following:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_PORT=5000

# Model Paths
MODEL_DIR=backend/model/distilbert
FINE_TUNED_MODEL_PATH=backend/model/sanity_model.bin

# Data Paths
PROCESSED_DATA_DIR=backend/data/processed
RAW_DATA_DIR=backend/data/raw

# Model Configuration
CONFIDENCE_THRESHOLD=0.70

# Frontend Configuration (optional)
VITE_API_URL=http://localhost:5000
```

**Note:** The frontend `.env` file should be in `frontend/.env` if you want to override the default API URL.

---

## 🚀 Running the Application

### Start Backend (Terminal 1)

```bash
# From project root
cd backend
python app.py

# Or if using virtual environment
python -m flask run --port=5000
```

Backend will run on: `http://localhost:5000`

### Start Frontend (Terminal 2)

```bash
# From frontend directory
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:3000`

---

## ✅ Verification

1. **Backend Health Check:**
   - Visit: `http://localhost:5000/health`
   - Should return: `{"status": "healthy"}`

2. **Frontend:**
   - Visit: `http://localhost:3000`
   - Should see the Sanity homepage

3. **Test Prediction:**
   - Enter some text in the frontend
   - Click "Analyze News"
   - Should see prediction results

---

## 📦 Project Structure

```
Sanity_V1/
├── backend/              # Flask backend
│   ├── app.py           # Main Flask app
│   ├── scripts/         # Training/evaluation scripts
│   ├── utils/           # Utilities (LLM, extractors)
│   ├── data/            # Datasets
│   ├── model/           # Trained models
│   └── requirements.txt # Backend dependencies
├── frontend/            # React frontend
│   ├── src/            # Source code
│   ├── package.json    # Frontend dependencies
│   └── .env            # Frontend env (optional)
├── requirements.txt     # Complete Python requirements
└── .env                # Main environment file
```

---

## 🐛 Troubleshooting

### Backend Issues

**Import Errors:**
```bash
# Make sure you're in the virtual environment
pip install -r requirements.txt
```

**Model Not Found:**
- Ensure model files exist in `backend/model/distilbert/`
- Run training script if needed: `python backend/scripts/train_model.py`

**Port Already in Use:**
- Change `FLASK_PORT` in `.env` or kill the process using port 5000

### Frontend Issues

**npm install fails:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API Connection Error:**
- Check `VITE_API_URL` in `frontend/.env`
- Ensure backend is running on port 5000
- Check CORS settings in backend

**Build Errors:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

---

## 📝 Next Steps After Setup

1. **Verify Backend:**
   - Test `/health` endpoint
   - Test `/predict` with sample text

2. **Verify Frontend:**
   - Open `http://localhost:3000`
   - Test text input
   - Test PDF upload
   - Test URL extraction

3. **Test Full Flow:**
   - Upload news article
   - View prediction
   - Ask follow-up questions in chat

4. **Production Build (Optional):**
   ```bash
   # Frontend
   cd frontend
   npm run build
   
   # Backend (using gunicorn)
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```

---

## 🔐 Security Notes

- Never commit `.env` file to git
- Keep `GROQ_API_KEY` secret
- Use environment variables in production
- Enable CORS only for trusted domains in production

---

## 📚 Additional Resources

- Backend API docs: `backend/docs/`
- Frontend docs: `frontend/README.md`
- Development plan: `Sanity_Development_Plan_v1.txt`

