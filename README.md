# Codex Platform

The Document Analyzer accepts PDF, Word or text files. A small React portal in
`frontend/` lets you select the backend URL, upload a document with an optional
prompt and view the returned analysis. Uploaded files are written to an
`uploads/` directory on the backend and results are stored in the same SQLite
database that holds customer and visitor records. The OpenRouter API key used by
the analyzer is configured directly in `backend/analyzer.py`.

