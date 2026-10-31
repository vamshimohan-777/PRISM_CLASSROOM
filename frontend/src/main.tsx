import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
import './curriculum.css';
import App from './App';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);

// Only register in production builds; the dev server serves modules that
// should never be cached.
if (import.meta.env.PROD && 'serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {
      /* offline shell is an enhancement; the app works without it */
    });
  });
}
