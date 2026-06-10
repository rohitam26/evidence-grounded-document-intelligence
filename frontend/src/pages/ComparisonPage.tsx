import React, { useState, useEffect } from 'react';
import { DocumentItem, ComparisonResult } from '../types';
import { api } from '../services/api';
import { GitCompare, AlertCircle, CheckCircle2 } from 'lucide-react';

interface ComparisonProps {
  documents: DocumentItem[];
}

export const ComparisonPage: React.FC<ComparisonProps> = ({ documents }) => {
  const [docA, setDocA] = useState<string>(documents[0]?.id || '');
  const [docB, setDocB] = useState<string>(documents[1]?.id || documents[0]?.id || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ComparisonResult | null>(null);

  useEffect(() => {
    if (!docA && documents.length > 0) {
      setDocA(documents[0].id);
    }
    if (!docB && documents.length > 1) {
      setDocB(documents[1].id);
    } else if (!docB && documents.length > 0) {
      setDocB(documents[0].id);
    }
  }, [documents, docA, docB]);

  const handleCompare = async () => {
    if (!docA || !docB) return;
    setLoading(true);
    try {
      const res = await api.compare(docA, docB);
      setResult(res);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '28px 32px', maxWidth: '1200px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#f1f5f9' }}>Cross-Document Comparison Studio</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
          Compare payment terms, termination rules, and governing law across contracts with side-by-side verified evidence.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '16px', alignItems: 'flex-end', backgroundColor: '#161b22', padding: '18px', borderRadius: '8px', border: '1px solid #27303d', marginBottom: '24px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '12px', color: '#8b949e', marginBottom: '6px' }}>Document A</label>
          <select 
            value={docA} 
            onChange={(e) => setDocA(e.target.value)}
            style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0e1117', border: '1px solid #21262d', borderRadius: '6px', color: '#f0f6fc', fontSize: '13px' }}
          >
            {documents.map((d) => (
              <option key={d.id} value={d.id}>{d.filename}</option>
            ))}
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '12px', color: '#8b949e', marginBottom: '6px' }}>Document B</label>
          <select 
            value={docB} 
            onChange={(e) => setDocB(e.target.value)}
            style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0e1117', border: '1px solid #21262d', borderRadius: '6px', color: '#f0f6fc', fontSize: '13px' }}
          >
            {documents.map((d) => (
              <option key={d.id} value={d.id}>{d.filename}</option>
            ))}
          </select>
        </div>

        <button 
          onClick={handleCompare}
          disabled={loading || !docA || !docB}
          style={{ 
            backgroundColor: '#2563eb', 
            color: '#ffffff', 
            padding: '10px 22px', 
            borderRadius: '6px', 
            border: 'none', 
            fontWeight: 600, 
            fontSize: '13px', 
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <GitCompare size={16} />
          {loading ? 'Analyzing Differences...' : 'Run Audit'}
        </button>
      </div>

      {result && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#f0f6fc' }}>
              Comparison: {result.document_a_name} vs {result.document_b_name}
            </h3>
            <span style={{ 
              fontSize: '12px', 
              fontWeight: 600, 
              padding: '4px 10px', 
              borderRadius: '4px',
              backgroundColor: result.conflict_count > 0 ? '#7f1d1d' : '#064e3b',
              color: result.conflict_count > 0 ? '#f87171' : '#34d399'
            }}>
              {result.conflict_count} Material Discrepancies
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {result.differences.map((diff, i) => (
              <div key={i} style={{ backgroundColor: '#161b22', border: `1px solid ${diff.is_conflict ? '#7f1d1d' : '#27303d'}`, borderRadius: '8px', padding: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {diff.is_conflict ? <AlertCircle size={16} color="#f87171" /> : <CheckCircle2 size={16} color="#34d399" />}
                    <span style={{ fontSize: '14px', fontWeight: 700, color: '#f0f6fc' }}>{diff.category}</span>
                  </div>
                  <span style={{ fontSize: '12px', color: diff.is_conflict ? '#f87171' : '#34d399', fontWeight: 600 }}>
                    {diff.difference_summary}
                  </span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginTop: '10px' }}>
                  <div style={{ backgroundColor: '#0e1117', padding: '12px', borderRadius: '6px', border: '1px solid #21262d' }}>
                    <div style={{ fontSize: '12px', fontWeight: 600, color: '#38bdf8', marginBottom: '4px' }}>
                      {result.document_a_name} (Page {diff.page_a})
                    </div>
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#f1f5f9', marginBottom: '4px' }}>Value: {diff.value_a}</div>
                    <p style={{ fontSize: '11px', color: '#8b949e' }}>"{diff.evidence_a}"</p>
                  </div>

                  <div style={{ backgroundColor: '#0e1117', padding: '12px', borderRadius: '6px', border: '1px solid #21262d' }}>
                    <div style={{ fontSize: '12px', fontWeight: 600, color: '#38bdf8', marginBottom: '4px' }}>
                      {result.document_b_name} (Page {diff.page_b})
                    </div>
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#f1f5f9', marginBottom: '4px' }}>Value: {diff.value_b}</div>
                    <p style={{ fontSize: '11px', color: '#8b949e' }}>"{diff.evidence_b}"</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
