import React, { useState, useEffect } from 'react';
import { Navigation } from './components/Navigation';
import { DashboardPage } from './pages/DashboardPage';
import { DocumentsPage } from './pages/DocumentsPage';
import { SearchPage } from './pages/SearchPage';
import { ChatPage } from './pages/ChatPage';
import { ComparisonPage } from './pages/ComparisonPage';
import { ExtractionPage } from './pages/ExtractionPage';
import { AgentPage } from './pages/AgentPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { SettingsPage } from './pages/SettingsPage';
import { api } from './services/api';
import { DocumentItem } from './types';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [documents, setDocuments] = useState<DocumentItem[]>([]);

  const loadDocuments = async () => {
    try {
      const res = await api.listDocuments();
      setDocuments(res.items || []);
    } catch (e) {
      console.error('Failed to load documents:', e);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <Navigation 
        currentTab={currentTab} 
        onSelectTab={setCurrentTab} 
        docCount={documents.length} 
      />

      <main style={{ flex: 1, height: '100vh', overflowY: 'auto', backgroundColor: '#0e1117' }}>
        {currentTab === 'dashboard' && <DashboardPage documents={documents} onNavigate={setCurrentTab} />}
        {currentTab === 'workspace' && <DocumentsPage documents={documents} onRefresh={loadDocuments} />}
        {currentTab === 'search' && <SearchPage />}
        {currentTab === 'chat' && <ChatPage />}
        {currentTab === 'comparison' && <ComparisonPage documents={documents} />}
        {currentTab === 'extraction' && <ExtractionPage documents={documents} />}
        {currentTab === 'agent' && <AgentPage />}
        {currentTab === 'evaluation' && <EvaluationPage />}
        {currentTab === 'settings' && <SettingsPage />}
      </main>
    </div>
  );
};

export default App;
