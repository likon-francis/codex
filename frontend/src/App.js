import React, { useState, useEffect, useRef } from 'react';


/**
 * Simple document analyzer portal. Allows selecting a backend URL,
 * uploading a document with an optional prompt and analysis type,
 * then viewing the returned analysis.
 */
function App() {
  const [baseUrl, setBaseUrl] = useState('http://localhost:8000');
  const [files, setFiles] = useState([]); // {file, status, result}
  const [prompt, setPrompt] = useState('');
  const [analysisType, setAnalysisType] = useState('');
  const [autoType, setAutoType] = useState(false);
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [presets, setPresets] = useState([]);
  const inputRef = useRef();


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

  const handleFiles = (list) => {
    const arr = Array.from(list).map((f) => ({ file: f, status: 'queued', result: '' }));
    setFiles(arr);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!files.length) return;
    setLoading(true);
    const updated = [...files];
    for (let i = 0; i < updated.length; i++) {
      updated[i].status = 'analyzing';
      setFiles([...updated]);
      const formData = new FormData();
      formData.append('file', updated[i].file);
      formData.append('prompt', prompt);
      formData.append('analysis_type', analysisType);
      formData.append('detect_type', autoType);
      try {
        const res = await fetch(`${baseUrl}/analyze`, {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        updated[i].result = data.result || JSON.stringify(data);
      } catch (err) {
        updated[i].result = 'Error contacting backend';
      }
      updated[i].status = 'done';
      setFiles([...updated]);
    }
    setLoading(false);
    loadDocuments();
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
        <div
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            handleFiles(e.dataTransfer.files);
          }}
          style={{ border: '2px dashed #ccc', padding: '1rem', marginBottom: '0.5rem', cursor: 'pointer' }}
          onClick={() => inputRef.current && inputRef.current.click()}
        >
          <p>Drop files here or click to select</p>
          <input
            ref={inputRef}
            type="file"
            multiple
            style={{ display: 'none' }}
            onChange={(e) => handleFiles(e.target.files)}
          />
        </div>
        {files.length > 0 && (
          <ul>
            {files.map((f, idx) => (
              <li key={idx}>{f.file.name} - {f.status}</li>
            ))}
          </ul>
        )}
        <div style={{ marginBottom: '0.5rem' }}>
          <select
            value={analysisType}
            onChange={(e) => {
              const val = e.target.value;
              setAnalysisType(val);
              const preset = presets.find((p) => p.type === val);
              if (preset) setPrompt(preset.prompt);
            }}
            style={{ width: '20rem' }}
          >
            <option value="">Select analysis type (optional)</option>
            {presets.map((p) => (
              <option key={p.type} value={p.type}>
                {p.type}
              </option>
            ))}
          </select>
          <label style={{ marginLeft: '0.5rem' }}>
            <input
              type="checkbox"
              checked={autoType}
              onChange={(e) => setAutoType(e.target.checked)}
            />
            Auto detect
          </label>

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
      {files.map((f, idx) => (
        f.result && (
          <div key={idx} style={{ marginTop: '1rem', whiteSpace: 'pre-wrap' }}>
            <h3>Result for {f.file.name}</h3>
            <pre>{f.result}</pre>
          </div>
        )
      ))}
      {files.some(f => f.result) && (
        <div style={{ marginTop: '1rem' }}>
          <button type="button" onClick={() => {
            const data = files.map(f => ({ filename: f.file.name, result: f.result }));
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'results.json';
            a.click();
            URL.revokeObjectURL(url);
          }}>Export JSON</button>
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
