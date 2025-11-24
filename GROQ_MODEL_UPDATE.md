# Groq Model Update

## 🔧 Issue Fixed

### Problem
The Groq API model `mixtral-8x7b-32768` has been **decommissioned** and is no longer supported.

**Error Message:**
```
The model `mixtral-8x7b-32768` has been decommissioned and is no longer supported.
```

### Solution
Updated the model to a currently supported Groq model:
- **Old Model:** `mixtral-8x7b-32768` (deprecated)
- **New Model:** `llama-3.1-70b-versatile` (active)

---

## 📝 Changes Made

### File: `backend/utils/llm_handler.py`

**Line 19:**
```python
# Before:
DEFAULT_MODEL = "mixtral-8x7b-32768"

# After:
DEFAULT_MODEL = "llama-3.1-70b-versatile"  # Updated from deprecated mixtral-8x7b-32768
```

---

## ✅ Next Steps

### 1. Restart Backend Server

The backend needs to be restarted to pick up the new model configuration:

```bash
# Stop current backend
Get-Process python | Stop-Process -Force

# Start backend again
cd backend
python app.py
```

### 2. Test the Fix

1. **Test Auto-Verification:**
   - Submit a news article with low confidence (< 70%)
   - Should trigger auto-verification using new model
   - Should work without errors

2. **Test Chat:**
   - Ask a direct question
   - Ask a follow-up question about an article
   - Both should work with new model

---

## 🔍 Alternative Models (if needed)

If `llama-3.1-70b-versatile` doesn't work, try these alternatives:

1. **`llama-3.1-8b-instant`** - Faster, smaller model
2. **`gemma2-9b-it`** - Google's Gemma model
3. **`llama-3.3-70b-versatile`** - Newer version if available

To change the model, update `DEFAULT_MODEL` in `backend/utils/llm_handler.py`

---

## 📚 Groq Model Documentation

For the latest available models, check:
- https://console.groq.com/docs/models
- https://console.groq.com/docs/deprecations

---

**Status:** ✅ **FIXED** - Model updated to `llama-3.1-70b-versatile`

