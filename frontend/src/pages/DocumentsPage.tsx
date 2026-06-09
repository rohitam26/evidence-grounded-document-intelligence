import React, { useState } from 'react';
import { DocumentItem } from '../types';
import { api } from '../services/api';
import { Upload, Trash2, RefreshCw, FileText, CheckCircle2, AlertCircle } from 'lucide-react';

interface DocumentsProps {
  documents: DocumentItem[];
  onRefresh: () => void;
}

export const DocumentsPage: React.FC<DocumentsProps> = ({ documents, onRefresh }) => {
  const [selectedDoc, setSelectedDoc] = useState<DocumentItem | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setUploading(true);
    setMessage(null);
    try {
      const res = await api.uploadDocument(file);
      setMessage(`Successfully processed ${file.name}`);
      onRefresh();
    } catch (err: any) {
      setMessage(`Upload error: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this document and all indexed vector chunks?')) return;
    await api.deleteDocument(id);
    if (selectedDoc?.id === id) setSelectedDoc(null);
    onRefresh();
  };

  const handleReprocess = async (id: string) => {
    await api.reprocessDocument(id);
    onRefresh();
  };

  return (
    <div style={{ padding: '28px 32px', maxWidth: '1300px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#f1f5f9' }}>Document Workspace</h2>
          <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
            Upload PDFs, DOCX, and images with automatic layout-aware chunking and vector indexing.
          </p>
        </div>

        <label style={{ 
          backgroundColor: '#2563eb', 
          color: '#ffffff', 
          padding: '8px 16px', 
          borderRadius: '6px', 
          fontSize: '13px', 
          fontWeight: 600, 
          cursor: uploading ? 'not-allowed' : 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <Upload size={16} />
          {uploading ? 'Processing File...' : 'Upload Document'}
          <input type="file" onChange={handleFileUpload} accept=".pdf,.docx,.png,.jpg,.jpeg" style={{ display: 'none' }} disabled={uploading} />
        </label>
      </div>

      {message && (
        <div style={{ padding: '10px 14px', backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '6px', marginBottom: '18px', fontSize: '13px', color: '#38bdf8' }}>
          {message}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Document List */}
        <div style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '18px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#f0f6fc', marginBottom: '14px' }}>Ingested Documents ({documents.length})</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '550px', overflowY: 'auto' }}>
            {documents.map((d) => (
              <div 
                key={d.id} 
                onClick={() => setSelectedDoc(d)}
                style={{ 
                  padding: '12px 14px', 
                  backgroundColor: selectedDoc?.id === d.id ? '#1e2632' : '#0e1117', 
                  border: `1px solid ${selectedDoc?.id === d.id ? '#38bdf8' : '#21262d'}`, 
                  borderRadius: '6px',
                  cursor: 'pointer',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <FileText size={18} color="#38bdf8" />
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#f0f6fc' }}>{d.filename}</div>
                    <div style={{ fontSize: '11px', color: '#8b949e' }}>
                      {d.page_count} pages • {(d.file_size_bytes / 1024).toFixed(1)} KB • {d.processing_duration_sec}s
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <button 
                    onClick={(e) => { e.stopPropagation(); handleReprocess(d.id); }}
                    title="Reprocess Document" 
                    style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#94a3b8' }}
                  >
                    <RefreshCw size={14} />
                  </button>
                  <button 
                    onClick={(e) => { e.stopPropagation(); handleDelete(d.id); }}
                    title="Delete Document" 
                    style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#f87171' }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Selected Document Metadata & Chunks Preview */}
        <div style={{ backgroundColor: '#161b22', border: '1px solid #27303d', borderRadius: '8px', padding: '18px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#f0f6fc', marginBottom: '14px' }}>
            {selectedDoc ? `Inspect: ${selectedDoc.filename}` : 'Document Inspection'}
          </h3>

          {selectedDoc ? (
            <div>
              <div style={{ padding: '12px', backgroundColor: '#0e1117', borderRadius: '6px', border: '1px solid #21262d', fontSize: '12px', marginBottom: '16px' }}>
                <div style={{ color: '#8b949e', marginBottom: '4px' }}>SHA-256 Hash: <code style={{ color: '#38bdf8' }}>{selectedDoc.content_hash}</code></div>
                <div style={{ color: '#8b949e', marginBottom: '4px' }}>Status: <span style={{ color: '#34d399', fontWeight: 600 }}>{selectedDoc.processing_status}</span></div>
                <div style={{ color: '#8b949e' }}>Pages: {selectedDoc.page_count} | Chunks: {selectedDoc.metadata_json?.chunk_count || 'N/A'}</div>
              </div>

              <h4 style={{ fontSize: '12px', fontWeight: 600, color: '#c9d1d9', marginBottom: '8px' }}>Layout Chunks Sample</h4>
              <div style={{ maxHeight: '350px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {selectedDoc.chunks && selectedDoc.chunks.length > 0 ? (
                  selectedDoc.chunks.map((c, i) => (
                    <div key={i} style={{ padding: '10px 12px', backgroundColor: '#0e1117', borderRadius: '4px', border: '1px solid #21262d', fontSize: '12px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748b', fontSize: '11px', marginBottom: '4px' }}>
                        <span>Page {c.page_number} • Section: {c.section_heading || 'Body'}</span>
                        <span style={{ textTransform: 'uppercase' }}>{c.source_type}</span>
                      </div>
                      <p style={{ color: '#e2e8f0', lineHeight: 1.4 }}>{c.content}</p>
                    </div>
                  ))
                ) : (
                  <div style={{ color: '#6e7681', fontSize: '12px' }}>Click on a document to inspect its parsed blocks.</div>
                )}
              </div>
            </div>
          ) : (
            <div style={{ padding: '40px', textAlign: 'center', color: '#6e7681', fontSize: '13px' }}>
              Select a document from the left list to review its SHA-256 hash, layout segmentation, and chunk contents.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
