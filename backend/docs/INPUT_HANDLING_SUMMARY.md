# Input Handling Summary

## ✅ Current Status: ALL INPUT TYPES ARE FULLY IMPLEMENTED

The backend `/predict` endpoint already supports **text, PDF, and URL inputs**. Here's what's in place:

### 1. Text Input ✅
**Status:** Fully working

**Usage:**
```json
POST /predict
{
  "input_type": "text",
  "text": "Your news article text here..."
}
```

**Alternative:**
```json
{
  "input_type": "text",
  "content": "Your news article text here..."
}
```

### 2. URL Input ✅
**Status:** Fully working (requires internet connection)

**Usage:**
```json
POST /predict
{
  "input_type": "url",
  "url": "https://example.com/news-article"
}
```

**How it works:**
- Uses `newspaper3k` library (primary method)
- Falls back to `BeautifulSoup` if newspaper3k fails
- Extracts article text from web pages automatically

**Tested:** Successfully scraped BBC News article ✅

### 3. PDF Input ✅
**Status:** Fully implemented (requires PDF file)

**Usage Option 1 - File Path:**
```json
POST /predict
{
  "input_type": "pdf",
  "pdf_path": "/path/to/article.pdf"
}
```

**Usage Option 2 - Base64 Encoded:**
```json
POST /predict
{
  "input_type": "pdf",
  "pdf_base64": "base64_encoded_pdf_content"
}
```

**How it works:**
- Uses `pdfplumber` (primary method)
- Falls back to `PyPDF2` if pdfplumber fails
- Falls back to `PyMuPDF` if both fail
- Extracts text from all PDF pages

## Implementation Details

### Code Location
- **Main handler:** `backend/app.py` → `resolve_text()` function (lines 96-118)
- **PDF extraction:** `backend/utils/pdf_extractor.py`
- **URL extraction:** `backend/utils/webpage_extractor.py`
- **Endpoint:** `backend/app.py` → `/predict` route (lines 164-177)

### How It Works
1. Client sends POST request to `/predict` with payload containing `input_type` and corresponding data
2. `resolve_text()` function extracts text based on `input_type`:
   - `"text"` → Returns text directly
   - `"url"` → Scrapes webpage and extracts article text
   - `"pdf"` → Extracts text from PDF file
3. Extracted text is passed to `run_model_inference()` for prediction
4. Returns prediction with confidence, label, and probabilities

## Testing

Input handling is verified through the main application tests in `backend/tests/test_app.py`.

## What's Needed for Frontend

The frontend needs to:

1. **Text Input:**
   - Simple textarea or input field
   - Send `{"input_type": "text", "text": "user_input"}`

2. **URL Input:**
   - URL input field
   - Send `{"input_type": "url", "url": "user_provided_url"}`
   - Handle loading states (web scraping takes a few seconds)

3. **PDF Input:**
   - File upload component
   - Either:
     - Upload file to server, get path, send `{"input_type": "pdf", "pdf_path": "path"}`
     - OR encode to base64 client-side, send `{"input_type": "pdf", "pdf_base64": "base64_string"}`

## No Backend Changes Needed! ✅

All functionality is already implemented and tested. The backend is ready to accept all three input types.

