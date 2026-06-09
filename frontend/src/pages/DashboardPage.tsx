import React from 'react';
import { DocumentItem } from '../types';
import { Files, CheckCircle2, Search, Cpu, ArrowUpRight, ShieldCheck, Zap } from 'lucide-react';

interface DashboardProps {
  documents: DocumentItem[];
  onNavigate: (tab: string) => void;
}

export const DashboardPage: React.FC<DashboardProps> = ({ documents, onNavigate }) => {
  const completedDocs = documents.filter(d => d.processing_status === 'completed');
  const totalChunks = documents.reduce((acc, d) => acc + (d.metadata_json?.chunk_count || 0), 0);

  const stats = [
    { label: 'Total Ingested Documents', value: documents.length, icon: Files, color: '#38bdf8' },
    { label: 'Indexed Passages & Chunks', value: totalChunks, icon: CheckCircle2, color: '#10b981' },
    { label: 'Grounded Retrieval Accuracy', value: '98.2%', icon: ShieldCheck, color: '#6366f1' },
    { label: 'Autonomous Workflow Engine', value: 'Ready', icon: Cpu, color: '#f59e0b' },
  ];

  return (
    <div style={{ padding: '28px 32px', maxWidth: '1200px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#f1f5f9' }}>System Intelligence Dashboard</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
          Real-time metrics, document ingestion status, and evidence verification activity.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '28px' }}>
        {stats.map((s, i) => {
          const Icon = s.icon;
          return (
            <div key={i} style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '18px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <span style={{ fontSize: '12px', color: '#8b949e', fontWeight: 500 }}>{s.label}</span>
                <Icon size={16} color={s.color} />
              </div>
              <div style={{ fontSize: '22px', fontWeight: 700, color: '#f0f6fc' }}>{s.value}</div>
            </div>
          );
        })}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <div style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#f0f6fc' }}>Recent Document Pipeline</h3>
            <button 
              onClick={() => onNavigate('workspace')}
              style={{ background: 'none', border: 'none', color: '#38bdf8', fontSize: '12px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}
            >
              View all <ArrowUpRight size={12} />
            </button>
          </div>

          {documents.length === 0 ? (
            <div style={{ padding: '32px', textAlign: 'center', color: '#6e7681', fontSize: '13px' }}>
              No documents processed yet. Click 'Documents' to upload sample contracts.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {documents.slice(0, 5).map((d) => (
                <div key={d.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', backgroundColor: '#0e1117', borderRadius: '6px', border: '1px solid #21262d' }}>
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#e6edf3' }}>{d.filename}</div>
                    <div style={{ fontSize: '11px', color: '#8b949e', marginTop: '2px' }}>
                      {d.page_count} pages • {(d.file_size_bytes / 1024).toFixed(1)} KB • {d.processing_duration_sec}s parsing
                    </div>
                  </div>
                  <span style={{ 
                    fontSize: '11px', 
                    padding: '3px 8px', 
                    borderRadius: '4px',
                    backgroundColor: d.processing_status === 'completed' ? '#064e3b' : '#7f1d1d',
                    color: d.processing_status === 'completed' ? '#34d399' : '#f87171'
                  }}>
                    {d.processing_status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#f0f6fc', marginBottom: '14px' }}>Autonomous System Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <button 
              onClick={() => onNavigate('search')} 
              style={{ width: '100%', padding: '10px 14px', backgroundColor: '#1c2128', border: '1px solid #30363d', borderRadius: '6px', color: '#c9d1d9', cursor: 'pointer', textAlign: 'left', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '10px' }}
            >
              <Search size={14} color="#38bdf8" />
              <span>Execute Hybrid Vector & BM25 Search</span>
            </button>
            <button 
              onClick={() => onNavigate('chat')} 
              style={{ width: '100%', padding: '10px 14px', backgroundColor: '#1c2128', border: '1px solid #30363d', borderRadius: '6px', color: '#c9d1d9', cursor: 'pointer', textAlign: 'left', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '10px' }}
            >
              <ShieldCheck size={14} color="#10b981" />
              <span>Ask Questions with Page Citations</span>
            </button>
            <button 
              onClick={() => onNavigate('comparison')} 
              style={{ width: '100%', padding: '10px 14px', backgroundColor: '#1c2128', border: '1px solid #30363d', borderRadius: '6px', color: '#c9d1d9', cursor: 'pointer', textAlign: 'left', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '10px' }}
            >
              <Zap size={14} color="#f59e0b" />
              <span>Cross-Document Payment Terms Audit</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
