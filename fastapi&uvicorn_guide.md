````markdown
# FastAPI + Uvicorn + Pydantic Basics

## Command Breakdown

```bash
uvicorn main:app --reload --port 8000 --host 0.0.0.0
````

### uvicorn

* High-performance ASGI web server for Python.
* Runs FastAPI/Starlette apps.

### main\:app

* **main** → Python module name (without `.py`).
* **app** → ASGI app instance inside the file.
* Together: Import `main.py` and use the `app` object.

### --reload

* Restarts server automatically on file changes.
* Development only.

### --port 8000

* Port to listen on (default: 8000).

### --host 0.0.0.0

* Listen on all interfaces, not just localhost.

---

## How `@app.post` Works with Pydantic

```python
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    ...
```

### Flow:

1. **Frontend sends**:

```json
{
    "question": "Plan a trip to Goa for 5 days"
}
```

2. **FastAPI matches route**:

   * Path `/query`
   * Method POST
   * Parameter type: `QueryRequest`

3. **Body parsing & validation**:

   * Reads JSON from request.
   * Validates keys & types using Pydantic.
   * Creates `QueryRequest` instance if valid.
   * Returns `422` error if invalid.

4. **Function receives**:

```python
query = QueryRequest(question="Plan a trip to Goa for 5 days")
print(query.question)  # "Plan a trip to Goa for 5 days"
```

**Takeaway**: FastAPI automatically parses JSON and instantiates your Pydantic model — no manual creation needed.