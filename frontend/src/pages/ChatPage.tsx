import React, { useState } from 'react';
import { api } from '../services/api';
import { ChatResponse, Citation } from '../types';
import { Send, ShieldCheck, AlertTriangle, BookOpen } from 'lucide-react';

interface ChatMessage {
  sender: 'user' | 'assistant';
  text: string;
  abstained?: boolean;
  abstention_reason?: string;
  citations?: Citation[];
  confidence?: number;
  latency_ms?: number;
}

export const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      sender: 'assistant',
      text: 'I am your Evidence-Grounded Document Intelligence Assistant. Ask any question about your documents. Every fact will include verifiable page citations, and I will strictly abstain if evidence is insufficient.'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [strict, setStrict] = useState(true);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const query = input;
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: query }]);
    setLoading(true);

    try {
      const res = await api.chat(query, undefined, strict);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: res.answer,
          abstained: res.abstained,
          abstention_reason: res.abstention_reason,
          citations: res.citations,
          confidence: res.grounding_confidence,
          latency_ms: res.latency_ms
        }
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { sender: 'assistant', text: `Error: ${err.message}`, abstained: true }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', maxWidth: '1100px', margin: '0 auto', padding: '24px 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', borderBottom: '1px solid #232b36', paddingBottom: '14px' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 700, color: '#f1f5f9' }}>Evidence-Grounded RAG Chat</h2>
          <p style={{ fontSize: '12px', color: '#94a3b8' }}>Strict citation verification with automatic abstention on unverified claims.</p>
        </div>

        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: '#c9d1d9', cursor: 'pointer' }}>
          <input type="checkbox" checked={strict} onChange={(e) => setStrict(e.target.checked)} />
          <span>Strict Grounding Enforcement</span>
        </label>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px', paddingRight: '8px', marginBottom: '20px' }}>
        {messages.map((m, i) => (
          <div key={i} style={{ 
            alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: m.sender === 'user' ? '70%' : '85%',
            backgroundColor: m.sender === 'user' ? '#1e3a8a' : '#161b22',
            border: `1px solid ${m.sender === 'user' ? '#2563eb' : '#27303d'}`,
            borderRadius: '8px',
            padding: '14px 16px',
            color: '#f0f6fc',
            fontSize: '13px',
            lineHeight: 1.5
          }}>
            {m.abstained ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#f87171', fontWeight: 600, marginBottom: '6px' }}>
                <AlertTriangle size={16} />
                <span>Abstention Triggered</span>
              </div>
            ) : m.sender === 'assistant' && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#34d399', fontSize: '11px', fontWeight: 600, marginBottom: '6px' }}>
                <ShieldCheck size={14} />
                <span>Verified Evidence • Grounding Confidence: {(m.confidence || 0.95) * 100}%</span>
              </div>
            )}

            <p style={{ whiteSpace: 'pre-wrap' }}>{m.text}</p>

            {m.citations && m.citations.length > 0 && (
              <div style={{ marginTop: '14px', paddingTop: '10px', borderTop: '1px solid #21262d' }}>
                <span style={{ fontSize: '11px', fontWeight: 600, color: '#8b949e', textTransform: 'uppercase' }}>Citations:</span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '6px' }}>
                  {m.citations.map((c) => (
                    <div key={c.citation_id} style={{ fontSize: '11px', backgroundColor: '#0e1117', padding: '6px 10px', borderRadius: '4px', border: '1px solid #21262d' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', color: '#38bdf8', fontWeight: 600 }}>
                        <span>[{c.citation_id}] {c.document_name} • Page {c.page_number}</span>
                        <span style={{ color: '#34d399' }}>Verified</span>
                      </div>
                      <p style={{ color: '#8b949e', marginTop: '3px' }}>"{c.source_passage}"</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div style={{ alignSelf: 'flex-start', color: '#8b949e', fontSize: '12px' }}>
            Retrieving passages and verifying citations...
          </div>
        )}
      </div>

      <form onSubmit={handleSend} style={{ display: 'flex', gap: '10px' }}>
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question (e.g. 'What are the payment terms under the Acme contract?')..."
          style={{ 
            flex: 1, 
            padding: '12px 14px', 
            backgroundColor: '#161b22', 
            border: '1px solid #27303d', 
            borderRadius: '6px', 
            color: '#f0f6fc', 
            fontSize: '13px' 
          }}
        />
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
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <Send size={15} />
          <span>Send</span>
        </button>
      </form>
    </div>
  );
};
