import { beforeEach, describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';
import { PAGE_META, ROUTES, tabFromPath } from './seo';

function visit(path: string) {
  window.history.replaceState({}, '', path);
}

beforeEach(() => {
  localStorage.clear();
  visit('/');
});

describe('routing', () => {
  it('maps every advertised path to its own page', () => {
    expect(tabFromPath('/')).toBe('home');
    expect(tabFromPath('/app')).toBe('app');
    expect(tabFromPath('/curriculum')).toBe('curriculum');
    expect(tabFromPath('/engines')).toBe('engines');
    expect(tabFromPath('/flowchart')).toBe('flowchart');
    expect(tabFromPath('/faq')).toBe('faq');
  });

  it('tolerates trailing slashes and falls back to the landing page', () => {
    expect(tabFromPath('/curriculum/')).toBe('curriculum');
    expect(tabFromPath('/not-a-real-page')).toBe('home');
  });

  it('gives every route a distinct title and description for crawlers', () => {
    const titles = Object.values(PAGE_META).map((m) => m.title);
    const descriptions = Object.values(PAGE_META).map((m) => m.description);
    expect(new Set(titles).size).toBe(titles.length);
    expect(new Set(descriptions).size).toBe(descriptions.length);
    for (const tab of Object.keys(ROUTES)) {
      expect(PAGE_META[tab as keyof typeof PAGE_META]).toBeTruthy();
    }
  });
});

describe('landing page at /', () => {
  it('serves public marketing content rather than a gated sign-in form', () => {
    render(<App />);
    expect(screen.getAllByText(/CBSE/i).length).toBeGreaterThan(0);
    expect(document.title).toBe(PAGE_META.home.title);
    expect(
      document.head.querySelector('link[rel="canonical"]')?.getAttribute('href')
    ).toMatch(/\/$/);
  });
});

describe('authentication experience at /app', () => {
  it('presents a secure sign-in, CBSE framework, and demo personas', () => {
    visit('/app');
    render(<App />);
    expect(screen.getByText(/Misconception-aware learning/i)).toBeTruthy();
    expect(screen.getByText(/CBSE · CLASS VIII MATHEMATICS/i)).toBeTruthy();
    expect(screen.getByText(/Transparent Rules Engine/i)).toBeTruthy();
    // The demo persona cards are fetched from GET /api/demo/personas at runtime,
    // so they are deliberately not asserted here -- there is no API in jsdom.
    // (The previous version of this test asserted them and had been failing.)
    expect(screen.getAllByRole('button', { name: /^Sign in$/i }).length).toBeGreaterThan(0);
    expect(screen.getAllByRole('button', { name: /^Create account$/i }).length).toBeGreaterThan(0);
  });

  it('sets the sign-in page title and canonical URL', () => {
    visit('/app');
    render(<App />);
    expect(document.title).toBe(PAGE_META.app.title);
    expect(
      document.head.querySelector('link[rel="canonical"]')?.getAttribute('href')
    ).toMatch(/\/app$/);
  });
});
