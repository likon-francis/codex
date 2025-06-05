# Document Analyzer Implementation Plan

This document tracks the main tasks required to build the Document Analyzer. Each
item is marked with its current status.

| Task | Status |
| --- | --- |
| Set up FastAPI backend with SQLite database | **Done** |
| Implement `/analyze` endpoint for file upload and OpenRouter call | **Done** |
| Store uploaded files in `uploads/` and save analysis results | **Done** |
| Provide `/documents` and `/documents/{id}` endpoints to fetch analyses | **Done** |
| Provide `/analysis-presets` endpoint listing built-in prompts | **Done** |
| Extract text from PDF, Word and plain text files | **Done** |
| React portal to choose backend URL, upload files, choose analysis type, prompt and view results | **Done** |
| Change analysis type input to a dropdown populated from presets | **Done** |
| Fetch preset analysis types for suggestions in the portal | **Done** |
| List previously analyzed documents with timestamps | **Done** |
| Persist OpenRouter API key via environment variable `OPENROUTER_API_KEY` | **Done** |
| Extend frontend `npm start` script with a real dev server | **Done** |
| Add authentication and user accounts | **Done** |
| Improve error handling and validation | **Done** |
| Add tests for backend API and frontend components | **Done** |


