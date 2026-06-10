import React, { useState } from 'react';
import { api } from '../services/api';
import { AgentRunResult } from '../types';
import { Cpu, Play, CheckCircle2, Clock, FileText } from 'lucide-react';

export const AgentPage: React.FC = () => {
  const [goal, setGoal] = useState('Audit contract payment terms and verify SLA commitments across documents');
  const [loading, setLoading] = useState(false);
  const [runResult, setRunResult] = useState<AgentRunResult | null>(null);

  const handleRunAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!goal.trim()) return;
    setLoading(true);
    try {
      const res = await api.runAgent(goal);
      setRunResult(res);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '28px 32px', maxWidth: '1200px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#f1f5f9' }}>Autonomous Document Intelligence Agent</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
          Multi-step stateful reasoning agent: planning, tool invocation, evidence extraction, citation validation, and certified report generation.
        </p>
      </div>

      <form onSubmit={handleRunAgent} style={{ display: 'flex', gap: '10px', backgroundColor: '#161b22', padding: '16px', borderRadius: '8px', border: '1px solid #27303d', marginBottom: '24px' }}>
        <input 
          type="text" 
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="State analysis goal (e.g. 'Compare Acme and Beta contracts for payment discrepancies and renewal terms')..."
          style={{ flex: 1, padding: '11px 14px', backgroundColor: '#0e1117', border: '1px solid #21262d', borderRadius: '6px', color: '#f0f6fc', fontSize: '13px' }}
        />
        <button 
          type="submit" 
          disabled={loading}
          style={{ 
            backgroundColor: '#2563eb', 
            color: '#ffffff', 
            padding: '0 22px', 
            borderRadius: '6px', 
            border: 'none', 
            fontWeight: 600, 
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <Play size={15} />
          <span>{loading ? 'Executing Agent Graph...' : 'Execute Agent'}</span>
        </button>
      </form>

      {runResult && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          {/* Step Execution Trace */}
          <div style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '18px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#f0f6fc' }}>Agent Step Trace ({runResult.steps.length} Steps)</h3>
              <span style={{ fontSize: '11px', color: '#34d399', backgroundColor: '#064e3b', padding: '3px 8px', borderRadius: '4px' }}>
                Completed in {runResult.duration_sec}s
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '550px', overflowY: 'auto' }}>
              {runResult.steps.map((s) => (
                <div key={s.step_number} style={{ padding: '10px 12px', backgroundColor: '#0e1117', borderRadius: '6px', border: '1px solid #21262d', fontSize: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', color: '#38bdf8', fontWeight: 600, marginBottom: '4px' }}>
                    <span>Step {s.step_number}: {s.action}</span>
                    {s.tool_name && <span style={{ color: '#f59e0b', fontSize: '11px' }}>Tool: {s.tool_name}</span>}
                  </div>
                  {s.tool_output && (
                    <div style={{ color: '#8b949e', fontSize: '11px', marginTop: '4px', backgroundColor: '#161b22', padding: '6px 8px', borderRadius: '4px' }}>
                      {typeof s.tool_output === 'object' ? JSON.stringify(s.tool_output) : String(s.tool_output)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Generated Certified Report */}
          <div style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '18px' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#f0f6fc', marginBottom: '14px' }}>Autonomously Generated Intelligence Report</h3>
            <div style={{ 
              backgroundColor: '#0e1117', 
              padding: '16px', 
              borderRadius: '6px', 
              border: '1px solid #21262d', 
              color: '#c9d1d9', 
              fontSize: '12px', 
              lineHeight: 1.6,
              maxHeight: '550px',
              overflowY: 'auto',
              whiteSpace: 'pre-wrap'
            }}>
              {runResult.final_output}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
