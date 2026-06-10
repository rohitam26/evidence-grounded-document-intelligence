import React, { useState } from 'react';
import { api } from '../services/api';
import { SearchResult } from '../types';
import { Search, SlidersHorizontal, BookOpen } from 'lucide-react';

export const SearchPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('hybrid');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [latency, setLatency] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await api.search(query, mode, 5);
      setResults(res.results || []);
      setLatency(res.retrieval_latency_ms || 0);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '28px 32px', maxWidth: '1100px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#f1f5f9' }}>Multi-Document AI Search</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
          Retrieve evidence across contracts and invoices using Dense Semantic vectors, Sparse BM25, and RRF Reranking.
        </p>
      </div>

      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <div style={{ flex: 1, position: 'relative' }}>
          <Search size={16} color="#64748b" style={{ position: 'absolute', left: '12px', top: '13px' }} />
          <input 
            type="text" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search across all contracts (e.g. 'payment terms Net 30', 'governing law', 'warranty SLA')..."
            style={{ 
              width: '100%', 
              padding: '11px 12px 11px 36px', 
              backgroundColor: '#161b22', 
              border: '1px solid #27303d', 
              borderRadius: '6px', 
              color: '#f0f6fc', 
              fontSize: '13px' 
            }}
          />
        </div>

        <select 
          value={mode} 
          onChange={(e) => setMode(e.target.value)}
          style={{ 
            backgroundColor: '#161b22', 
            border: '1px solid #27303d', 
            borderRadius: '6px', 
            color: '#c9d1d9', 
            padding: '0 12px', 
            fontSize: '13px' 
          }}
        >
          <option value="hybrid">Hybrid (Dense + BM25 + RRF)</option>
          <option value="dense">Dense Vectors (Qdrant)</option>
          <option value="sparse">Sparse BM25 Keyword</option>
        </select>

        <button 
          type="submit" 
          disabled={loading}
          style={{ 
            backgroundColor: '#2563eb', 
            color: '#ffffff', 
            padding: '0 20px', 
            borderRadius: '6px', 
            border: 'none', 
            fontWeight: 600, 
            fontSize: '13px', 
            cursor: 'pointer' 
          }}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {latency !== null && (
        <div style={{ fontSize: '12px', color: '#8b949e', marginBottom: '16px' }}>
          Found {results.length} ranked passages in <span style={{ color: '#38bdf8' }}>{latency}ms</span>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {results.map((r, i) => (
          <div key={i} style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <BookOpen size={14} color="#38bdf8" />
                <span style={{ fontSize: '13px', fontWeight: 600, color: '#f0f6fc' }}>{r.document_name}</span>
                <span style={{ fontSize: '11px', color: '#8b949e', backgroundColor: '#21262d', padding: '2px 6px', borderRadius: '4px' }}>
                  Page {r.page_number}
                </span>
                {r.section_heading && (
                  <span style={{ fontSize: '11px', color: '#64748b' }}>• {r.section_heading}</span>
                )}
              </div>
              <span style={{ fontSize: '11px', color: '#34d399', fontWeight: 600 }}>
                Score: {r.score.toFixed(4)} ({r.retrieval_method})
              </span>
            </div>

            <p style={{ fontSize: '13px', color: '#c9d1d9', lineHeight: 1.5, backgroundColor: '#0e1117', padding: '10px 12px', borderRadius: '4px', border: '1px solid #21262d' }}>
              {r.content}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
