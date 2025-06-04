# Frontend

This directory contains a very small React application used to interact with the
Codex backend. It uses [Vite](https://vitejs.dev/) for development.

## Getting started

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the development server (defaults to `http://localhost:5173`):

   ```bash
   npm run dev
   ```

The application provides simple pages for each backend module (customers,
door access, IoT devices, and visitors). Each page now includes a small form to
add new records which are sent to the backend via fetch calls. Navigation links
are available in the top navbar.
