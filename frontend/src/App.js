import React, { useState } from 'react';

/**
 * Simple document analyzer portal. Allows selecting a backend URL,
 * uploading a document with an optional prompt and viewing the
 * returned analysis.
 */
function App() {
  const [baseUrl, setBaseUrl] = useState('http://localhost:8000');
  const [file, setFile] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('prompt', prompt);
    try {
      const res = await fetch(`${baseUrl}/analyze`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setResult(data.result || JSON.stringify(data));
    } catch (err) {
      setResult('Error contacting backend');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '1rem', fontFamily: 'sans-serif' }}>
      <h1>Codex Document Analyzer</h1>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Backend URL:
          <input
            type="text"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
            style={{ marginLeft: '0.5rem', width: '20rem' }}
          />
        </label>
      </div>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '0.5rem' }}>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>
        <div style={{ marginBottom: '0.5rem' }}>
          <textarea
            placeholder="Optional prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={3}
            style={{ width: '20rem' }}
          />
        </div>
        <button type="submit" disabled={loading}>Analyze</button>
      </form>

      {loading && <p>Analyzing...</p>}
      {result && (
        <div style={{ marginTop: '1rem', whiteSpace: 'pre-wrap' }}>
          <h3>Result</h3>
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
