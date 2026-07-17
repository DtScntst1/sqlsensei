import { useState } from 'react';
import axios from 'axios';
import ReactECharts from 'echarts-for-react';
import { FiSend, FiDatabase, FiKey } from 'react-icons/fi';
import './index.css';

function App() {
  const [apiKey, setApiKey] = useState('');
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAsk = async () => {
    if (!apiKey) {
      setError('Please enter your free Groq API Key.');
      return;
    }
    if (!question) {
      setError('Please enter a question.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await axios.post('https://sqlsensei.onrender.com/api/v1/query', {
        question: question,
        api_key: apiKey
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'An error occurred while generating the query.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>SQLSensei</h1>
        <p>Talk to your database in plain English. Get SQL and ECharts instantly.</p>
      </div>

      <div className="glass-panel">
        <div style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <FiKey size={24} color="var(--accent-purple)" />
          <input 
            type="password" 
            placeholder="gsk_... (Enter your free Groq API Key)" 
            value={apiKey} 
            onChange={(e) => setApiKey(e.target.value)} 
          />
        </div>

        <div className="chat-input-container">
          <input 
            type="text" 
            placeholder="e.g. Show me the total sales amount by product name as a bar chart" 
            value={question} 
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
          />
          <button onClick={handleAsk} disabled={loading}>
            {loading ? <span className="loader"></span> : <><FiSend /> Ask</>}
          </button>
        </div>
        
        {error && <div style={{ color: '#ef4444', marginTop: '1rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px' }}>{error}</div>}
      </div>

      {result && (
        <div className="results-grid">
          <div className="glass-panel">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
              <FiDatabase color="var(--accent-blue)" /> Generated SQL
            </h3>
            <div className="code-block">
              {result.sql}
            </div>
            
            <h3 style={{ marginTop: '2rem', marginBottom: '1rem' }}>Raw Data Preview</h3>
            <div className="code-block" style={{ fontSize: '0.85rem' }}>
              {JSON.stringify(result.data.slice(0, 5), null, 2)}
            </div>
          </div>

          <div className="glass-panel">
            <h3 style={{ marginBottom: '1rem' }}>Visualization</h3>
            {result.chart_config ? (
              <div className="chart-container">
                <ReactECharts option={result.chart_config} style={{ height: '100%', width: '100%' }} />
              </div>
            ) : (
              <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                LLM did not generate a valid chart configuration for this query.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
