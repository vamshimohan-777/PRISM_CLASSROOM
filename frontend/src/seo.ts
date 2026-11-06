/**
 * Routing table and per-page metadata.
 *
 * Navigation used to be `useState` only, with no URL behind it. sitemap.xml
 * advertised /curriculum, /flowchart and /faq, but the SPA fallback served
 * index.html for every path and the app always booted to the sign-in screen,
 * so a crawler following the sitemap landed on the same gated page four times
 * and every route shared one <title>. These paths are now real, and each sets
 * its own title, description and canonical URL.
 */
export type ActiveTab = 'app' | 'home' | 'curriculum' | 'faq' | 'engines' | 'flowchart';

export const ROUTES: Record<ActiveTab, string> = {
  home: '/',
  app: '/app',
  curriculum: '/curriculum',
  engines: '/engines',
  flowchart: '/flowchart',
  faq: '/faq',
};

const PATH_TO_TAB = new Map<string, ActiveTab>(
  (Object.entries(ROUTES) as [ActiveTab, string][]).map(([tab, path]) => [path, tab])
);

/** Resolve a pathname to a tab, tolerating trailing slashes and unknown paths. */
export function tabFromPath(pathname: string): ActiveTab {
  const normalised = pathname.replace(/\/+$/, '') || '/';
  return PATH_TO_TAB.get(normalised) ?? 'home';
}

export const SITE_ORIGIN: string =
  (import.meta.env.VITE_SITE_ORIGIN as string | undefined) ||
  (typeof window !== 'undefined' ? window.location.origin : 'https://prism-classroom.onrender.com');

type PageMeta = { title: string; description: string };

export const PAGE_META: Record<ActiveTab, PageMeta> = {
  home: {
    title: 'PRISM Classroom — Misconception-Aware Adaptive Learning for Indian Schools',
    description:
      'PRISM Classroom diagnoses why a CBSE Class VIII learner got a question wrong, not just that they did, and compiles the evidence into teacher-approved small-group intervention pods.',
  },
  app: {
    title: 'Sign In — PRISM Classroom Learning Workspace',
    description:
      'Sign in to the PRISM Classroom workspace: adaptive CBSE Class VIII Mathematics activities for learners and the Teacher Intervention Compiler for educators.',
  },
  curriculum: {
    title: 'CBSE Class VIII Mathematics Curriculum Explorer — PRISM Classroom',
    description:
      'Explore all eight NCERT Class VIII Mathematics chapters, their learning outcomes and the prerequisite concept graph PRISM uses to route learners.',
  },
  engines: {
    title: 'Engines Studio — Search, Answer and Generative Engines — PRISM Classroom',
    description:
      'Try the three PRISM engines: curriculum-aware indexed search, a step-by-step NCERT answer engine with verification, and a generator for questions, remediation guides and lesson plans.',
  },
  flowchart: {
    title: 'System Architecture Flowchart — PRISM Classroom',
    description:
      'The closed-loop PRISM data lifecycle: learner attempt ingestion, deterministic rules engine scoring, prerequisite DAG routing and the Teacher Intervention Compiler.',
  },
  faq: {
    title: 'Help & FAQ — How PRISM Classroom Works',
    description:
      'Answers to common questions about PRISM Classroom: how misconceptions are diagnosed, how mastery is scored, how teachers stay in control, and how offline classrooms are supported.',
  },
};

function upsertMeta(attribute: 'name' | 'property', key: string, content: string) {
  let tag = document.head.querySelector<HTMLMetaElement>(`meta[${attribute}="${key}"]`);
  if (!tag) {
    tag = document.createElement('meta');
    tag.setAttribute(attribute, key);
    document.head.appendChild(tag);
  }
  tag.setAttribute('content', content);
}

function upsertCanonical(href: string) {
  let link = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]');
  if (!link) {
    link = document.createElement('link');
    link.setAttribute('rel', 'canonical');
    document.head.appendChild(link);
  }
  link.setAttribute('href', href);
}

/** Point the document's crawler-facing metadata at the active route. */
export function applyPageMeta(tab: ActiveTab) {
  const meta = PAGE_META[tab];
  if (!meta) return;
  const url = `${SITE_ORIGIN}${ROUTES[tab]}`;

  document.title = meta.title;
  upsertMeta('name', 'description', meta.description);
  upsertMeta('property', 'og:title', meta.title);
  upsertMeta('property', 'og:description', meta.description);
  upsertMeta('property', 'og:url', url);
  upsertMeta('name', 'twitter:title', meta.title);
  upsertMeta('name', 'twitter:description', meta.description);
  upsertCanonical(url);
}
