import { StrictMode, Component, type ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
import '@xyflow/react/dist/style.css';
import './i18n';
import './index.css';
import App from './App';

class ErrorBoundary extends Component<{ children: ReactNode }, { err: boolean }> {
  state = { err: false };
  static getDerivedStateFromError() {
    return { err: true };
  }
  componentDidCatch() {
    setTimeout(() => this.setState({ err: false }), 2000);
  }
  render() {
    if (this.state.err) {
      return (
        <div className="flex h-full items-center justify-center bg-noc-bg text-slate-300">
          Reconnecting…
        </div>
      );
    }
    return this.props.children;
  }
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
