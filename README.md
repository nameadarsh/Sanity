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

**Note:** Large files (model files >100MB and dataset CSV files >50MB) are excluded from the repository due to GitHub file size limits. You'll need to:
- Download the DistilBERT model or train your own (see Training section)
- Add your own datasets to `backend/data/raw/` for training

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
2. **Text Extraction**: System extracts text from the input format using specialized libraries
3. **Text Cleaning**: Extracted text is cleaned and normalized before processing
4. **Model Prediction**: Fine-tuned DistilBERT classifies as Real/Fake with confidence
5. **Auto-Verification**: If confidence < 70%, Groq LLM verifies the prediction
6. **Result Display**: User sees final prediction (LLM if verified, model otherwise)
7. **Interactive Q&A**: Users can ask follow-up questions about the article

## 🔧 Technical Stack & Modules

### Backend Technologies

#### Core Framework & Server
- **Flask** (≥3.0.0): Lightweight Python web framework for building REST APIs
- **Flask-CORS** (≥4.0.0): Cross-Origin Resource Sharing support for frontend-backend communication
- **python-dotenv** (≥1.0.0): Environment variable management from `.env` files
- **uvicorn** (≥0.24.0): ASGI server for production deployment
- **gunicorn** (≥21.2.0): WSGI HTTP server for production

#### Machine Learning & NLP
- **PyTorch** (≥2.1.0): Deep learning framework for model inference
- **Transformers** (≥4.35.0): Hugging Face library for DistilBERT model loading and tokenization
- **accelerate** (≥0.25.0): Accelerated training and inference utilities
- **scikit-learn** (≥1.3.0): Machine learning utilities for data preprocessing and evaluation
- **numpy** (≥1.24.0): Numerical computing for array operations
- **pandas** (≥2.1.0): Data manipulation and analysis for dataset processing

#### Natural Language Processing
- **NLTK** (≥3.8.1): Natural Language Toolkit for text preprocessing
  - **punkt**: Sentence tokenization
  - **punkt_tab**: Updated tokenizer data
  - **wordnet**: Lexical database for lemmatization
  - **stopwords**: Common stop words removal
  - **omw-1.4**: Open Multilingual Wordnet

#### PDF Text Extraction
The application uses a **multi-library fallback approach** for robust PDF text extraction:

1. **pdfplumber** (≥0.10.0) - **Primary Method**
   - High-quality text extraction with layout preservation
   - Handles complex PDF structures and tables
   - Extracts text from both file paths and byte streams
   - Best for most PDF formats

2. **PyPDF2** (≥3.0.0) - **Fallback Method 1**
   - Lightweight PDF manipulation library
   - Good for simple PDF documents
   - Works with both file paths and byte streams
   - Used when pdfplumber fails

3. **PyMuPDF** (≥1.23.1) - **Fallback Method 2** (Optional)
   - Fast PDF rendering and text extraction
   - Excellent for scanned PDFs and complex layouts
   - Only works with file paths (not byte streams)
   - Used as final fallback if other methods fail

**Extraction Flow:**
```
PDF Input → pdfplumber (try) → PyPDF2 (try) → PyMuPDF (try) → Error
```

**Implementation Location:** `backend/utils/pdf_extractor.py`

#### URL/Web Scraping
The application uses a **dual-library approach** for extracting article content from URLs:

1. **newspaper3k** (≥0.2.8) - **Primary Method**
   - Specialized library for article extraction from news websites
   - Automatically identifies and extracts main article content
   - Removes ads, navigation, and other non-article elements
   - Handles article metadata (title, author, publish date)
   - Best for news websites and blogs

2. **BeautifulSoup4** (≥4.12.0) + **requests** (≥2.31.0) - **Fallback Method**
   - **requests**: HTTP library for fetching web pages
   - **BeautifulSoup**: HTML parsing library for extracting text
   - Extracts all paragraph (`<p>`) tags from HTML
   - More generic approach, works with any website
   - Used when newspaper3k fails or is unavailable

**Extraction Flow:**
```
URL Input → newspaper3k (try) → BeautifulSoup + requests (try) → Error
```

**Implementation Location:** `backend/utils/webpage_extractor.py`

#### Text Processing & Cleaning
- **text_cleaner.py**: Custom utility module for cleaning text before LLM processing
  - Removes excessive whitespace
  - Normalizes line breaks
  - Truncates text to maximum length (default: 8000 chars)
  - Word-boundary aware truncation

#### LLM Integration
- **Groq API**: Fast inference API for LLM interactions
  - **Default Model**: `llama-3.3-70b-versatile` (70B parameter model)
  - **API Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
  - **Three Prompt Flows**:
    1. Direct questions (general queries)
    2. Follow-up questions (context-aware)
    3. Low-confidence verification (auto-verification)
- **requests** (≥2.31.0): HTTP client for API calls

#### Logging & Monitoring
- **loguru** (≥0.7.0): Advanced logging library with structured logging
- Custom logger utilities in `backend/utils/logger.py`

#### Testing
- **pytest** (≥8.0.0): Testing framework for backend unit tests
- **tqdm** (≥4.66.0): Progress bars for long-running operations

### Frontend Technologies

#### Core Framework
- **React** (^18.2.0): JavaScript library for building user interfaces
- **React DOM** (^18.2.0): React renderer for web browsers
- **Vite** (^5.0.8): Fast build tool and development server

#### Routing & Navigation
- **React Router DOM** (^6.20.0): Declarative routing for React applications

#### State Management
- **Zustand** (^4.4.7): Lightweight state management library
  - `usePredictionStore`: Manages prediction results, chat history, loading states
  - `useThemeStore`: Manages light/dark theme with localStorage persistence

#### HTTP Client
- **Axios** (^1.6.2): Promise-based HTTP client for API requests
  - Wrapper in `frontend/src/lib/api.js` for backend communication
  - Automatic error handling and request/response interceptors

#### Styling & UI
- **TailwindCSS** (^3.3.6): Utility-first CSS framework
  - Dark mode support via class strategy
  - Custom theme extensions (colors, animations, transitions)
  - Fully responsive design system
- **PostCSS** (^8.4.32): CSS transformation tool
- **Autoprefixer** (^10.4.16): Automatic vendor prefixing

#### Animations
- **Framer Motion** (^10.16.16): Production-ready motion library for React
  - Page transitions
  - Component animations (fade, slide, scale)
  - Stagger effects for lists
  - Smooth hover interactions

#### UI Components
- **@headlessui/react** (^1.7.17): Unstyled, accessible UI components
- **@heroicons/react** (^2.1.1): Beautiful hand-crafted SVG icons
- **lucide-react** (^0.294.0): Additional icon library

#### Development Tools
- **ESLint** (^8.55.0): JavaScript linter
- **eslint-plugin-react** (^7.33.2): React-specific linting rules
- **eslint-plugin-react-hooks** (^4.6.0): React Hooks linting rules
- **@vitejs/plugin-react** (^4.2.1): Vite plugin for React support

### Data Processing Pipeline

#### Preprocessing (`backend/scripts/preprocess_data.py`)
1. **Load Datasets**: Merges real and fake news CSV files
2. **Text Cleaning**:
   - Lowercase conversion
   - Special character removal
   - URL and email removal
   - Whitespace normalization
3. **Tokenization**: NLTK word tokenization
4. **Stopword Removal**: Removes common stop words
5. **Lemmatization**: Reduces words to their root forms
6. **Dataset Splitting**: Train/validation/test split (80/10/10)

#### Model Training (`backend/scripts/train_model.py`)
- **Base Model**: `distilbert-base-uncased` from Hugging Face
- **Fine-tuning**: Custom training on news classification dataset
- **Framework**: Hugging Face Trainer API
- **Output**: Fine-tuned model saved to `backend/model/distilbert/`

#### Model Inference (`backend/app.py`)
- **Tokenization**: DistilBERT tokenizer with max length 512
- **Inference**: PyTorch model forward pass
- **Post-processing**: Softmax for probability distribution
- **Confidence Calculation**: Maximum probability as confidence score

### LLM Prompt System

#### Prompt Templates (`backend/utils/prompts.py`)
1. **PROMPT_DIRECT_QUESTION**: For general user queries
   - System prompt: Expert AI assistant with fact-checking emphasis
   - Output format: Bullet points, no hallucinations

2. **PROMPT_FOLLOWUP_NEWS**: For context-aware follow-up questions
   - Includes: Article text, model prediction, verification summary
   - System prompt: Answer based strictly on provided context

3. **PROMPT_LOW_CONFIDENCE_VERIFY**: For auto-verification
   - System prompt: Fact-checking model with strict verification
   - Output format: "Prediction: Real/Fake\nReasoning: <2-3 sentences>"

#### LLM Handler (`backend/utils/llm_handler.py`)
- **GroqClient**: Wrapper class for Groq API interactions
- **Methods**:
  - `call_llm()`: Generic LLM call with prompt template
  - `verify_article()`: Auto-verification for low-confidence predictions
  - `answer_question()`: Q&A with context routing
- **Error Handling**: Robust error handling with fallbacks
- **Response Parsing**: Extracts prediction and reasoning from LLM output

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

### PDF Extraction Configuration

The PDF extraction system automatically tries multiple libraries in order:
1. **pdfplumber** (recommended for best results)
2. **PyPDF2** (fallback for simple PDFs)
3. **PyMuPDF** (fallback for complex/scanned PDFs)

All three libraries are included in `backend/requirements.txt`. If you want to disable PyMuPDF (optional dependency), you can remove it from requirements, and the system will use the first two methods.

### URL Scraping Configuration

The URL extraction system uses:
1. **newspaper3k** (primary - best for news sites)
2. **BeautifulSoup + requests** (fallback - works with any website)

Both are included in `backend/requirements.txt`. The system automatically falls back if newspaper3k fails.

**Note**: Some websites may block automated scraping. If you encounter issues:
- Check if the website requires authentication
- Verify the URL is publicly accessible
- Consider adding custom headers or delays for rate limiting

## 🐛 Troubleshooting

### Backend Issues

- **Model not loading**: Ensure `MODEL_DIR` in `.env` points to the correct model directory
- **Groq API errors**: Check your API key and model availability
- **Port already in use**: Change `FLASK_PORT` in `.env`
- **PDF extraction fails**: 
  - Ensure all PDF libraries are installed: `pip install pdfplumber PyPDF2 PyMuPDF`
  - Check if the PDF is password-protected or corrupted
  - Verify file permissions
- **URL scraping fails**:
  - Check if the website is accessible and not blocking bots
  - Verify the URL is a valid news article link
  - Some sites may require custom headers (modify `webpage_extractor.py`)
- **NLTK data missing**: Run the NLTK download command in the installation section

### Frontend Issues

- **API connection errors**: Verify `VITE_API_URL` in `.env` matches backend URL
- **Build errors**: Run `npm install` again in the frontend directory
- **Theme not persisting**: Check browser localStorage permissions
- **Animations not working**: Ensure Framer Motion is properly installed

## 📝 License

ISC

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👤 Author

**nameadarsh**

- GitHub: [@nameadarsh](https://github.com/nameadarsh)

## 🙏 Acknowledgments

### Core Technologies
- [Hugging Face Transformers](https://huggingface.co/transformers/) - Pre-trained models and tokenizers
- [Groq API](https://console.groq.com/) - Fast LLM inference
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [Flask](https://flask.palletsprojects.com/) - Web framework

### Frontend Libraries
- [React](https://react.dev/) - UI library
- [TailwindCSS](https://tailwindcss.com/) - CSS framework
- [Framer Motion](https://www.framer.com/motion/) - Animation library
- [Zustand](https://github.com/pmndrs/zustand) - State management
- [Vite](https://vitejs.dev/) - Build tool

### Data Processing
- [NLTK](https://www.nltk.org/) - Natural language processing
- [pandas](https://pandas.pydata.org/) - Data manipulation
- [scikit-learn](https://scikit-learn.org/) - Machine learning utilities

### PDF Extraction
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF text extraction
- [PyPDF2](https://github.com/py-pdf/PyPDF2) - PDF manipulation
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - Fast PDF processing

### Web Scraping
- [newspaper3k](https://github.com/codelucas/newspaper) - Article extraction
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [requests](https://requests.readthedocs.io/) - HTTP library

---

<div align="center">

Made with ❤️ for truth and accuracy in news

</div>
