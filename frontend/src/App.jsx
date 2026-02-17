import { useState } from 'react';
import { Routes, Route, NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, Upload, MessageSquare, Search,
  GitCompare, FileText, Zap, ChevronLeft, ChevronRight, Sun, Moon
} from 'lucide-react';
import { ToastProvider } from './components/Toast';

import UploadPage from './pages/UploadPage';
import DocumentPage from './pages/DocumentPage';
import ChatPage from './pages/ChatPage';
import DashboardPage from './pages/DashboardPage';
import ComparePage from './pages/ComparePage';
import SearchPage from './pages/SearchPage';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload', icon: Upload, label: 'Documents' },
  { to: '/search', icon: Search, label: 'Search' },
  { to: '/compare', icon: GitCompare, label: 'Compare' },
];

function Sidebar({ collapsed, onToggle }) {
  const location = useLocation();
  const [theme, setTheme] = useState('dark');

  const toggleTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    document.documentElement.setAttribute('data-theme', next);
  };

  return (
    <aside className={`sidebar fixed left-0 top-0 h-screen bg-[var(--bg-surface)] border-r border-[var(--border-subtle)] flex flex-col z-50 overflow-hidden
      ${collapsed ? 'sidebar-collapsed' : 'sidebar-expanded'}`}
    >
      {/* Logo */}
      <div className="p-5 border-b border-[var(--border-subtle)]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center glow-accent flex-shrink-0">
            <Zap className="w-5 h-5 text-white" />
          </div>
          {!collapsed && (
            <div className="animate-fade-in">
              <h1 className="text-lg font-bold gradient-text whitespace-nowrap">DocInsights</h1>
              <p className="text-[10px] text-[var(--text-muted)] tracking-widest uppercase">AI Platform</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map(({ to, icon: Icon, label }) => {
          const isActive = to === '/' ? location.pathname === '/' : location.pathname.startsWith(to);
          return (
            <NavLink key={to} to={to} title={collapsed ? label : undefined}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200
              ${isActive
                ? 'bg-primary-600/20 text-primary-400 shadow-lg shadow-primary-500/10 border-glow'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-elevated)]'
              }`}>
              <Icon className="w-5 h-5 flex-shrink-0" />
              {!collapsed && <span className="whitespace-nowrap">{label}</span>}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer controls */}
      <div className="p-3 space-y-2 border-t border-[var(--border-subtle)]">
        {/* Theme toggle */}
        <button onClick={toggleTheme}
          className={`flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] transition-all`}>
          {theme === 'dark' ? <Sun className="w-5 h-5 flex-shrink-0" /> : <Moon className="w-5 h-5 flex-shrink-0" />}
          {!collapsed && <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>}
        </button>

        {/* Collapse toggle */}
        <button onClick={onToggle}
          className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] transition-all">
          {collapsed ? <ChevronRight className="w-5 h-5 flex-shrink-0" /> : <ChevronLeft className="w-5 h-5 flex-shrink-0" />}
          {!collapsed && <span>Collapse</span>}
        </button>

        {!collapsed && (
          <div className="px-3 py-3 rounded-xl bg-gradient-to-r from-primary-900/40 to-purple-900/40 border border-primary-800/30 animate-fade-in">
            <p className="text-xs text-primary-300 font-medium">v2.0 — AI-Powered</p>
            <p className="text-[10px] text-[var(--text-muted)] mt-0.5">RAG • Semantic Search • Insights</p>
          </div>
        )}
      </div>
    </aside>
  );
}

export default function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <ToastProvider>
      <div className="flex min-h-screen">
        <Sidebar collapsed={sidebarCollapsed} onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} />
        <main className={`flex-1 transition-all duration-[400ms] ease-in-out p-8 ${sidebarCollapsed ? 'ml-[72px]' : 'ml-[260px]'}`}>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/documents/:id" element={<DocumentPage />} />
            <Route path="/documents/:id/chat" element={<ChatPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/compare" element={<ComparePage />} />
          </Routes>
        </main>
      </div>
    </ToastProvider>
  );
}
