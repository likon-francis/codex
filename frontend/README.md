# Frontend

This React app provides a document analyzer portal with the following features:

- **Drag-and-drop upload area** supporting multiple files with a status list.
- **Document type selector** or automatic detection via the backend.
- **Prompt template picker** loaded from `/analysis-presets` with an editable
  Markdown field.
- **Status tracker** indicating queued, analyzing and completed files.
- **Result viewer** that can switch between summary, full text or table view.
- **Export** the results as JSON, CSV or printable PDF.

Enter the backend URL, drop your files, optionally select a prompt template or
edit the prompt, choose the analysis type or enable auto detection and then view
the returned analysis.

Run the app in development mode using Parcel:

```bash
npm install
npm run start
```
