# Frontend

This React app provides a small portal for uploading documents to the backend
analyzer. Enter the backend URL, choose a file, optionally supply a prompt and
select the analysis type from a dropdown, then view the returned analysis.
Available analysis types are fetched from the backend via `/analysis-presets`
and populate the dropdown list.

Run the app in development mode using Parcel:

```bash
npm install
npm run start
```
