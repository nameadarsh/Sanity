# Sanity: Real vs Fake News Detection Web App

<div align="center">

![Sanity Logo](https://img.shields.io/badge/Sanity-AI%20News%20Verification-blue?style=for-the-badge)

**An AI-driven web application that detects whether news articles are real or fake using a fine-tuned DistilBERT model and Groq API for verification.**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API Reference](#-api-endpoints)

</div>

---

## 🚀 Features

- **🤖 AI-Powered Detection**: Fine-tuned DistilBERT model for accurate news classification
- **📄 Multi-Format Input**: Accept text, PDF files, or URLs for analysis
- **✅ Auto-Verification**: Low-confidence predictions automatically verified via Groq LLM API
- **💬 Interactive Q&A**: Ask follow-up questions about articles or general queries
- **🎨 Modern UI**: Beautiful React frontend with TailwindCSS and Framer Motion animations
- **🌓 Dark Mode**: Full light/dark theme support
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 📁 Project Structure

```
Sanity_V1/
├── backend/                    # Flask backend
│   ├── app.py                 # Main Flask application
│   ├── scripts/               # Utility scripts
│   │   ├── preprocess_data.py # Data preprocessing
│   │   ├── train_model.py     # Model training
│   │   ├── evaluate_model.py  # Model evaluation
│   │   ├── check_groq_models.py # Groq model checker
│   │   └── auto_update_model.py # Auto-update Groq model
│   ├── utils/                 # Utility modules
│   │   ├── llm_handler.py     # Groq API integration
│   │   ├── prompts.py         # LLM prompt templates
│   │   ├── pdf_extractor.py   # PDF text extraction
│   │   ├── webpage_extractor.py # URL scraping
│   │   ├── text_cleaner.py    # Text cleaning utilities
│   │   └── logger.py          # Logging utilities
│   ├── data/                  # Datasets
│   │   ├── raw/               # Raw datasets
│   │   └── processed/         # Processed datasets
│   ├── model/                 # Trained models
│   │   └── distilbert/        # DistilBERT model files
│   ├── tests/                 # Unit tests
│   ├── docs/                  # Backend documentation
│   └── logs/                  # Application logs
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── store/             # Zustand state management
│   │   ├── lib/               # API utilities
│   │   └── hooks/             # Custom React hooks
│   └── package.json
├── docs/                      # Project documentation
├── .env                       # Environment variables (create this)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🛠️ Quick Start

### Prerequisites

- **Python 3.9+** (for backend)
- **Node.js 18+** and **npm** (for frontend)
- **Groq API Key** ([Get one here](https://console.groq.com/))

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/nameadarsh/Sanity.git
cd Sanity
```

#### 2. Backend Setup

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Download NLTK data (required for preprocessing)
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('wordnet'); nltk.download('stopwords')"
```

#### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

#### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_PORT=5000

# Model Configuration
MODEL_DIR=backend/model/distilbert
FINE_TUNED_MODEL_PATH=backend/model/sanity_model.bin
PROCESSED_DATA_DIR=backend/data/processed
RAW_DATA_DIR=backend/data/raw
CONFIDENCE_THRESHOLD=0.70

# Frontend API URL
VITE_API_URL=http://localhost:5000
```

#### 5. Prepare Data & Train Model (Optional)

If you want to train your own model:

```bash
# Preprocess data
python backend/scripts/preprocess_data.py

# Train model
python backend/scripts/train_model.py --epochs 3 --batch-size 8

# Evaluate model
python backend/scripts/evaluate_model.py
```

### Running the Application

#### Start Backend

```bash
cd backend
python app.py
```

The backend will be available at `http://localhost:5000`

#### Start Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🔌 API Endpoints

### Health Check
```http
GET /health
```
Returns server status and model readiness.

### Predict News
```http
POST /predict
Content-Type: application/json

{
  "input_type": "text",  // "text", "pdf", or "url"
  "text": "Your news article text here...",
  // OR for PDF:
  "input_type": "pdf",
  "pdf_path": "/path/to/file.pdf",
  // OR for URL:
  "input_type": "url",
  "url": "https://example.com/news-article"
}
```

**Response:**
```json
{
  "label": "Real",
  "confidence": 0.85,
  "probabilities": {
    "real": 0.85,
    "fake": 0.15
  },
  "needs_verification": false,
  "context_id": "uuid-here",
  "auto_verification": {
    "prediction": "Real",
    "reasoning": "Verified reasoning..."
  }
}
```

### Verify Article (Manual)
```http
POST /verify
Content-Type: application/json

{
  "article_text": "Article content here..."
}
```

### Ask Questions
```http
POST /ask
Content-Type: application/json

{
  "question": "Is this article reliable?",
  "context_id": "uuid-from-prediction"  // Optional: for follow-up questions
}
```

## 📚 Documentation

- **[Setup Guide](SETUP_GUIDE.md)** - Detailed setup instructions
- **[Input Handling](backend/docs/INPUT_HANDLING_SUMMARY.md)** - How to handle different input types
- **[LLM Prompt Flows](backend/docs/LLM_PROMPT_FLOWS.md)** - LLM integration details
- **[Development Plan](Sanity_Development_Plan_v1.txt)** - Original development plan

## 🧪 Testing

### Backend Tests

```bash
pytest backend/tests/
```

### Manual Testing

1. Start both backend and frontend servers
2. Navigate to `http://localhost:3000`
3. Try different input types (text, PDF, URL)
4. Test the chat interface for Q&A

## 🎯 How It Works

1. **Input Processing**: User submits news via text, PDF, or URL
2. **Text Extraction**: System extracts text from the input format
3. **Model Prediction**: Fine-tuned DistilBERT classifies as Real/Fake with confidence
4. **Auto-Verification**: If confidence < 70%, Groq LLM verifies the prediction
5. **Result Display**: User sees final prediction (LLM if verified, model otherwise)
6. **Interactive Q&A**: Users can ask follow-up questions about the article

## 🔧 Configuration

### Confidence Threshold

Adjust the confidence threshold in `.env`:
```env
CONFIDENCE_THRESHOLD=0.70  # Auto-verify if confidence < 0.70
```

### Groq Model

The default model is `llama-3.3-70b-versatile`. To check available models:
```bash
python backend/scripts/check_groq_models.py
```

To auto-update the model:
```bash
python backend/scripts/auto_update_model.py
```

## 🐛 Troubleshooting

### Backend Issues

- **Model not loading**: Ensure `MODEL_DIR` in `.env` points to the correct model directory
- **Groq API errors**: Check your API key and model availability
- **Port already in use**: Change `FLASK_PORT` in `.env`

### Frontend Issues

- **API connection errors**: Verify `VITE_API_URL` in `.env` matches backend URL
- **Build errors**: Run `npm install` again in the frontend directory

## 📝 License

ISC

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👤 Author

**nameadarsh**

- GitHub: [@nameadarsh](https://github.com/nameadarsh)

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Groq API](https://console.groq.com/)
- [React](https://react.dev/)
- [TailwindCSS](https://tailwindcss.com/)
- [Framer Motion](https://www.framer.com/motion/)

---

<div align="center">

Made with ❤️ for truth and accuracy in news

</div>
