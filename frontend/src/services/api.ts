import { DocumentItem, SearchResult, ChatResponse, ExtractionResult, ComparisonResult, AgentRunResult } from '../types';

const API_BASE = '/api/v1';

export const api = {
  // Health
  async getHealth() {
    const res = await fetch(`${API_BASE}/ready`);
    return res.json();
  },

  // Documents
  async listDocuments(): Promise<{ total: number; items: DocumentItem[] }> {
    const res = await fetch(`${API_BASE}/documents`);
    return res.json();
  },

  async getDocument(id: string): Promise<DocumentItem> {
    const res = await fetch(`${API_BASE}/documents/${id}`);
    return res.json();
  },

  async uploadDocument(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      body: formData,
    });
    return res.json();
  },

  async deleteDocument(id: string): Promise<any> {
    const res = await fetch(`${API_BASE}/documents/${id}`, {
      method: 'DELETE',
    });
    return res.json();
  },

  async reprocessDocument(id: string): Promise<any> {
    const res = await fetch(`${API_BASE}/documents/${id}/reprocess`, {
      method: 'POST',
    });
    return res.json();
  },

  // Search
  async search(query: string, mode = 'hybrid', topK = 5): Promise<{ results: SearchResult[]; retrieval_latency_ms: number }> {
    let actualMode = mode;
    let actualTopK = topK;
    if (typeof mode === 'number') {
      actualTopK = mode;
      actualMode = typeof topK === 'string' ? topK : 'hybrid';
    }
    const res = await fetch(`${API_BASE}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, mode: actualMode, top_k: actualTopK }),
    });
    return res.json();
  },

  // Chat (Grounded RAG)
  async chat(message: string, documentIds?: string[], strictGrounding = true): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, document_ids: documentIds, strict_grounding: strictGrounding }),
    });
    return res.json();
  },

  // Extraction
  async extract(documentId: string, schemaName = 'contract'): Promise<ExtractionResult> {
    const res = await fetch(`${API_BASE}/extract`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ document_id: documentId, schema_name: schemaName }),
    });
    return res.json();
  },

  // Comparison
  async compare(docA: string, docB: string): Promise<ComparisonResult> {
    const res = await fetch(`${API_BASE}/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ document_a_id: docA, document_b_id: docB }),
    });
    return res.json();
  },

  // Agent Workflows
  async runAgent(goal: string, documentIds?: string[]): Promise<AgentRunResult> {
    const res = await fetch(`${API_BASE}/agent/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal, document_ids: documentIds }),
    });
    return res.json();
  },

  async getReports(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/reports`);
    return res.json();
  }
};
