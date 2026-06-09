import React from 'react';
import { 
  LayoutDashboard, 
  Files, 
  Search, 
  MessageSquare, 
  GitCompare, 
  FileCode, 
  Cpu, 
  BarChart3, 
  Settings,
  ShieldCheck
} from 'lucide-react';

interface NavigationProps {
  currentTab: string;
  onSelectTab: (tab: string) => void;
  docCount: number;
}

export const Navigation: React.FC<NavigationProps> = ({ currentTab, onSelectTab, docCount }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'workspace', label: 'Documents', icon: Files, badge: docCount },
    { id: 'search', label: 'AI Search', icon: Search },
    { id: 'chat', label: 'Evidence Chat', icon: MessageSquare },
    { id: 'comparison', label: 'Doc Comparison', icon: GitCompare },
    { id: 'extraction', label: 'Extraction Studio', icon: FileCode },
    { id: 'agent', label: 'Autonomous Agent', icon: Cpu },
    { id: 'evaluation', label: 'Evaluation & Benchmarks', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside style={{ width: '250px', backgroundColor: '#131820', borderRight: '1px solid #232b36', display: 'flex', flexDirection: 'column', height: '100vh', position: 'sticky', top: 0 }}>
      <div style={{ padding: '20px 18px', borderBottom: '1px solid #232b36', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{ width: '32px', height: '32px', borderRadius: '6px', background: 'linear-gradient(135deg, #2563eb, #38bdf8)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <ShieldCheck size={18} color="#ffffff" />
        </div>
        <div>
          <h1 style={{ fontSize: '14px', fontWeight: 700, letterSpacing: '-0.3px', color: '#f8fafc' }}>DocIntelligence</h1>
          <span style={{ fontSize: '10px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.6px', fontWeight: 600 }}>Evidence Core</span>
        </div>
      </div>

      <nav style={{ flex: 1, padding: '12px 10px', display: 'flex', flexDirection: 'column', gap: '4px', overflowY: 'auto' }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                padding: '9px 12px',
                borderRadius: '6px',
                border: 'none',
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '13px',
                fontWeight: isActive ? 600 : 500,
                color: isActive ? '#38bdf8' : '#94a3b8',
                backgroundColor: isActive ? '#1e293b' : 'transparent',
                transition: 'all 0.15s ease'
              }}
            >
              <Icon size={16} color={isActive ? '#38bdf8' : '#64748b'} />
              <span style={{ flex: 1 }}>{item.label}</span>
              {item.badge !== undefined && item.badge > 0 && (
                <span style={{ fontSize: '10px', backgroundColor: '#334155', color: '#f1f5f9', padding: '1px 6px', borderRadius: '10px' }}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      <div style={{ padding: '14px 18px', borderTop: '1px solid #232b36', fontSize: '11px', color: '#64748b' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '7px', height: '7px', borderRadius: '50%', backgroundColor: '#10b981' }}></span>
          <span>Engine Online (Local)</span>
        </div>
        <div style={{ marginTop: '4px', fontSize: '10px', color: '#475569' }}>v1.0.0 Enterprise</div>
      </div>
    </aside>
  );
};
