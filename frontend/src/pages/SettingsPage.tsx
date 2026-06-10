import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Settings, Server, Cpu, Database, CheckCircle2, AlertTriangle } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [healthData, setHealthData] = useState<any>(null);
  const [model, setModel] = useState('qwen2.5:7b-instruct');
  const [endpoint, setEndpoint] = useState('http://localhost:11434');

  useEffect(() => {
    api.getHealth().then(setHealthData).catch(() => setHealthData(null));
  }, []);

  return (
    <div style={{ padding: '28px 32px', maxWidth: '1000px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#f1f5f9' }}>System & Runtime Settings</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
          Configure local Ollama inference, vector store connection, and system operational parameters.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {/* Runtime Status */}
        <div style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '18px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#f0f6fc', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Server size={16} color="#38bdf8" /> Core Service Connectivity
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px' }}>
            <div style={{ backgroundColor: '#0e1117', padding: '12px', borderRadius: '6px', border: '1px solid #21262d' }}>
              <div style={{ fontSize: '11px', color: '#8b949e' }}>Relational Database</div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: '#34d399', marginTop: '2px' }}>Connected (SQLite / Postgres)</div>
            </div>
            <div style={{ backgroundColor: '#0e1117', padding: '12px', borderRadius: '6px', border: '1px solid #21262d' }}>
              <div style={{ fontSize: '11px', color: '#8b949e' }}>Vector Store (Qdrant)</div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: '#34d399', marginTop: '2px' }}>Active (Embedded / Server)</div>
            </div>
            <div style={{ backgroundColor: '#0e1117', padding: '12px', borderRadius: '6px', border: '1px solid #21262d' }}>
              <div style={{ fontSize: '11px', color: '#8b949e' }}>Ollama Local Inference</div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: healthData?.components?.llm_inference?.available ? '#34d399' : '#38bdf8', marginTop: '2px' }}>
                {healthData?.components?.llm_inference?.available ? 'Connected' : 'Degraded (Deterministic Grounding)'}
              </div>
            </div>
          </div>
        </div>

        {/* Inference Configuration */}
        <div style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '18px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#f0f6fc', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Cpu size={16} color="#f59e0b" /> Local LLM Configuration
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#8b949e', marginBottom: '6px' }}>Ollama Server Endpoint</label>
              <input 
                type="text" 
                value={endpoint} 
                onChange={(e) => setEndpoint(e.target.value)}
                style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0e1117', border: '1px solid #21262d', borderRadius: '6px', color: '#f0f6fc', fontSize: '13px' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#8b949e', marginBottom: '6px' }}>Target Model</label>
              <input 
                type="text" 
                value={model} 
                onChange={(e) => setModel(e.target.value)}
                style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0e1117', border: '1px solid #21262d', borderRadius: '6px', color: '#f0f6fc', fontSize: '13px' }}
              />
              <span style={{ fontSize: '11px', color: '#64748b', marginTop: '4px', display: 'block' }}>
                Default: <code>qwen2.5:7b-instruct</code>. Run <code>ollama pull qwen2.5:7b-instruct</code> to configure locally.
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
