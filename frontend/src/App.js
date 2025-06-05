import React, { useState, useEffect } from 'react';
/**
 * Simple document analyzer portal. Allows selecting a backend URL,
 * uploading a document with an optional prompt and analysis type,
 * then viewing the returned analysis.
 */
function App() {
  const [baseUrl, setBaseUrl] = useState('http://localhost:8000');
  const [file, setFile] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [analysisType, setAnalysisType] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [presets, setPresets] = useState([]);

  const loadDocuments = async () => {
    try {
      const res = await fetch(`${baseUrl}/documents`);
      const data = await res.json();
      setDocuments(data);
    } catch {
      setDocuments([]);
    }
  };

  useEffect(() => {
    loadDocuments();
    const loadPresets = async () => {
      try {
        const res = await fetch(`${baseUrl}/analysis-presets`);
        const data = await res.json();
        setPresets(data);
      } catch {
        setPresets([]);
      }
    };
    loadPresets();
  }, [baseUrl]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('prompt', prompt);
    formData.append('analysis_type', analysisType);
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
          <select
            value={analysisType}
            onChange={(e) => setAnalysisType(e.target.value)}
            style={{ width: '20rem' }}
          >
            <option value="">Select analysis type (optional)</option>
            {presets.map((p) => (
              <option key={p.type} value={p.type}>
                {p.type}
              </option>
            ))}
          </select>
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

      <div style={{ marginTop: '2rem' }}>
        <h3>Previous Documents</h3>
        <button type="button" onClick={loadDocuments} style={{ marginBottom: '0.5rem' }}>
          Refresh
        </button>
        <ul>
          {documents.map((doc) => (
            <li key={doc.id} style={{ marginBottom: '0.25rem' }}>
              {doc.filename} ({doc.analysis_type || 'N/A'}) -{' '}
              {doc.created_at && new Date(doc.created_at).toLocaleString()}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
