# LLM Prompt Flows Implementation

## Overview

The backend now implements **3 separate LLM prompt flows** for different interaction scenarios:

1. **Direct Question** - General queries not related to articles
2. **Follow-up Question** - Questions about previously processed articles
3. **Low Confidence Auto-Verification** - Automatic verification when model confidence < 0.70

## Implementation Details

### Files Created/Modified

1. **`backend/utils/prompts.py`** - Contains all 3 prompt templates
2. **`backend/utils/llm_handler.py`** - Updated with `call_llm()` method and new flow logic
3. **`backend/utils/text_cleaner.py`** - Text cleaning utility for prompts
4. **`backend/app.py`** - Updated endpoints with context storage and auto-verification

### Flow 1: Direct Question

**Condition:** User asks a general question (no article context)

**Endpoint:** `POST /ask`

**Request:**
```json
{
  "question": "What is inflation?"
}
```

**Response:**
```json
{
  "answer": "• Inflation is the rate at which prices for goods and services rise...\n• It's measured by indices like CPI...\n..."
}
```

**Prompt Used:** `PROMPT_DIRECT_QUESTION`

### Flow 2: Follow-up Question About Article

**Condition:** User asks about a previously processed article

**Endpoint:** `POST /ask`

**Request Option 1 (using context_id):**
```json
{
  "context_id": "uuid-from-predict-response",
  "question": "Why is it fake?"
}
```

**Request Option 2 (explicit context):**
```json
{
  "article_text": "Article content...",
  "model_prediction": "Fake",
  "verification_summary": "Verification reasoning...",
  "question": "What is the source?"
}
```

**Response:**
```json
{
  "answer": "Based on the article content provided, the source appears to be..."
}
```

**Prompt Used:** `PROMPT_FOLLOWUP_NEWS`

### Flow 3: Low Confidence Auto-Verification

**Condition:** Model confidence < 0.70 (automatic, no user request)

**Endpoint:** `POST /predict` (automatic)

**Behavior:**
- When `/predict` returns confidence < 0.70, system automatically calls LLM
- LLM provides updated prediction and reasoning
- Results included in response

**Response includes:**
```json
{
  "label": "Fake",
  "confidence": 0.65,
  "needs_verification": true,
  "auto_verification": {
    "prediction": "Fake",
    "reasoning": "The article contains several factual inaccuracies..."
  },
  "context_id": "uuid-for-follow-ups"
}
```

**Prompt Used:** `PROMPT_LOW_CONFIDENCE_VERIFY`

## Context Storage

The backend stores article context in memory (`_article_contexts` dict) after each prediction:

- **Key:** `context_id` (UUID, returned in `/predict` response)
- **Value:** Dict containing:
  - `article_text`: Original article text
  - `model_prediction`: Model's prediction (Real/Fake)
  - `model_confidence`: Confidence score
  - `verification`: LLM verification reasoning (if auto-verified)
  - `verification_prediction`: LLM's prediction (if auto-verified)

## API Endpoints

### POST /predict

Predicts if news is real/fake. Auto-verifies if confidence < 0.70.

**Request:**
```json
{
  "input_type": "text",
  "text": "Article text here..."
}
```

**Response:**
```json
{
  "article_text": "...",
  "context_id": "uuid-here",
  "label": "Real",
  "confidence": 0.92,
  "needs_verification": false,
  "probabilities": {"fake": 0.08, "real": 0.92}
}
```

If confidence < 0.70, also includes:
```json
{
  "auto_verification": {
    "prediction": "Real",
    "reasoning": "Factual reasoning here..."
  }
}
```

### POST /ask

Handles both direct questions and follow-up questions.

**Direct Question:**
```json
{
  "question": "What is cyber security?"
}
```

**Follow-up Question:**
```json
{
  "context_id": "uuid-from-predict",
  "question": "Why is it fake?"
}
```

**Response:**
```json
{
  "answer": "Answer text here..."
}
```

### POST /verify

Manual verification (uses low-confidence prompt).

**Request:**
```json
{
  "article_text": "Article to verify..."
}
```

**Response:**
```json
{
  "prediction": "Real",
  "reasoning": "Factual reasoning...",
  "raw": {...}
}
```

## Text Cleaning

All text sent to LLM is cleaned via `clean_text_for_prompt()`:
- Removes excessive whitespace
- Normalizes line breaks
- Truncates to 8000 characters if needed (at word boundaries)

## Error Handling

- Missing `GROQ_API_KEY`: Returns 503
- Groq API errors: Returns 502
- Invalid requests: Returns 400
- All errors are logged

## Testing

To test the flows:

1. **Direct Question:**
   ```bash
   curl -X POST http://localhost:5000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is inflation?"}'
   ```

2. **Follow-up Question:**
   ```bash
   # First, get context_id from /predict
   # Then use it in /ask
   curl -X POST http://localhost:5000/ask \
     -H "Content-Type: application/json" \
     -d '{"context_id": "uuid-here", "question": "Why is it fake?"}'
   ```

3. **Auto-Verification:**
   - Send article with low confidence prediction
   - System automatically verifies and includes result

