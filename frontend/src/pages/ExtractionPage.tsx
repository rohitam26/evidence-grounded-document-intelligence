import React, { useState, useEffect } from 'react';
import { DocumentItem, ExtractionResult } from '../types';
import { api } from '../services/api';
import { FileCode, Download, ShieldCheck, AlertCircle } from 'lucide-react';

interface ExtractionProps {
  documents: DocumentItem[];
}

export const ExtractionPage: React.FC<ExtractionProps> = ({ documents }) => {
  const [docId, setDocId] = useState<string>(documents[0]?.id || '');
  const [schema, setSchema] = useState<string>('contract');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ExtractionResult | null>(null);

  useEffect(() => {
    if (!docId && documents.length > 0) {
      setDocId(documents[0].id);
    }
  }, [documents, docId]);

  const handleExtract = async () => {
    if (!docId) return;
    setLoading(true);
    try {
      const res = await api.extract(docId, schema);
      setResult(res);
    } finally {
      setLoading(false);
    }
  };

  const handleExportJSON = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `docintel_extracted_${result.schema_name}_${docId.slice(0, 8)}.json`;
    a.click();
  };

  return (
    <div style={{ padding: '28px 32px', maxWidth: '1200px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#f1f5f9' }}>Structured Information Extraction Studio</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
          Extract validated Pydantic schema entities with page-level citations and completeness scoring.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr auto', gap: '16px', alignItems: 'flex-end', backgroundColor: '#161b22', padding: '18px', borderRadius: '8px', border: '1px solid #27303d', marginBottom: '24px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '12px', color: '#8b949e', marginBottom: '6px' }}>Select Target Document</label>
          <select 
            value={docId} 
            onChange={(e) => setDocId(e.target.value)}
            style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0e1117', border: '1px solid #21262d', borderRadius: '6px', color: '#f0f6fc', fontSize: '13px' }}
          >
            {documents.map((d) => (
              <option key={d.id} value={d.id}>{d.filename}</option>
            ))}
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '12px', color: '#8b949e', marginBottom: '6px' }}>Extraction Schema</label>
          <select 
            value={schema} 
            onChange={(e) => setSchema(e.target.value)}
            style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0e1117', border: '1px solid #21262d', borderRadius: '6px', color: '#f0f6fc', fontSize: '13px' }}
          >
            <option value="contract">Commercial Contract Schema</option>
            <option value="invoice">Standard Invoice Schema</option>
          </select>
        </div>

        <button 
          onClick={handleExtract}
          disabled={loading || !docId}
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
          <FileCode size={16} />
          {loading ? 'Extracting Fields...' : 'Extract Fields'}
        </button>
      </div>

      {result && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#f0f6fc' }}>Extraction Results</h3>
              <span style={{ fontSize: '12px', color: '#34d399', fontWeight: 600, backgroundColor: '#064e3b', padding: '3px 8px', borderRadius: '4px' }}>
                Completeness: {(result.completeness_score * 100).toFixed(0)}%
              </span>
            </div>

            <button 
              onClick={handleExportJSON}
              style={{ background: 'none', border: '1px solid #30363d', color: '#c9d1d9', padding: '6px 14px', borderRadius: '6px', cursor: 'pointer', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <Download size={14} /> Export JSON
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '14px' }}>
            {Object.entries(result.fields).map(([fieldName, fieldData]) => (
              <div key={fieldName} style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8', textTransform: 'capitalize' }}>
                    {fieldName.replace(/_/g, ' ')}
                  </span>
                  <span style={{ 
                    fontSize: '11px', 
                    padding: '2px 6px', 
                    borderRadius: '4px',
                    backgroundColor: fieldData.validation_status === 'valid' ? '#064e3b' : '#7f1d1d',
                    color: fieldData.validation_status === 'valid' ? '#34d399' : '#f87171'
                  }}>
                    {fieldData.validation_status}
                  </span>
                </div>

                <div style={{ fontSize: '14px', fontWeight: 600, color: '#f1f5f9', marginBottom: '6px' }}>
                  {fieldData.extracted_value !== null ? String(fieldData.extracted_value) : '<Not Found>'}
                </div>

                <div style={{ fontSize: '11px', color: '#8b949e', backgroundColor: '#0e1117', padding: '8px 10px', borderRadius: '4px', border: '1px solid #21262d' }}>
                  <span style={{ color: '#64748b', fontWeight: 600 }}>Page {fieldData.page_number} Citation:</span> "{fieldData.supporting_passage}"
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
