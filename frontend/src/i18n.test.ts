/**
 * Guards translation completeness.
 *
 * The Engines Studio shipped with every visible string hardcoded in English
 * while importing TRANSLATIONS and never reading it, so the language switcher
 * silently changed only the navigation. These tests fail the build if a key is
 * added to one language but not the others, or left untranslated.
 */
import { describe, expect, it } from 'vitest';
import { TRANSLATIONS, type Language } from './translations';
import { CHAPTER_TRANSLATIONS } from './localization';
import { ENGINES_TEXT, enginesText } from './enginesText';
import { MISCONCEPTION_LABELS, ROUTE_LABELS, TEACHER_TEXT } from './teacherText';

const LANGS: Language[] = ['en', 'hi', 'te'];
const NON_EN = LANGS.filter((l) => l !== 'en');

/** Latin letters are expected in brand names and parenthetical English terms. */
const UNTRANSLATED_ALLOWLIST = new Set(['emailPlaceholder']);

describe('TRANSLATIONS', () => {
  it('defines the same keys in every language', () => {
    const keysets = LANGS.map((l) => new Set(Object.keys(TRANSLATIONS[l])));
    const union = new Set(keysets.flatMap((s) => [...s]));
    for (const [i, lang] of LANGS.entries()) {
      const missing = [...union].filter((k) => !keysets[i].has(k));
      expect(missing, `missing in ${lang}`).toEqual([]);
    }
  });
});

describe('ENGINES_TEXT', () => {
  it('defines the same keys in every language', () => {
    const keysets = LANGS.map((l) => new Set(Object.keys(ENGINES_TEXT[l])));
    const union = new Set(keysets.flatMap((s) => [...s]));
    for (const [i, lang] of LANGS.entries()) {
      const missing = [...union].filter((k) => !keysets[i].has(k));
      expect(missing, `missing in ${lang}`).toEqual([]);
    }
  });

  it('has no empty strings', () => {
    for (const lang of LANGS) {
      for (const [key, value] of Object.entries(ENGINES_TEXT[lang])) {
        expect(String(value).trim(), `${lang}.${key}`).not.toBe('');
      }
    }
  });

  it('actually translates Hindi and Telugu rather than copying English', () => {
    for (const lang of NON_EN) {
      const script = lang === 'hi' ? /[ऀ-ॿ]/ : /[ఀ-౿]/;
      const copied: string[] = [];
      for (const [key, value] of Object.entries(ENGINES_TEXT[lang])) {
        if (UNTRANSLATED_ALLOWLIST.has(key)) continue;
        // Every string long enough to carry meaning must contain native script.
        if (String(value).length > 3 && !script.test(String(value))) copied.push(key);
      }
      expect(copied, `untranslated ${lang} keys`).toEqual([]);
    }
  });

  it('falls back to English for an unknown language', () => {
    expect(enginesText('xx' as Language)).toBe(ENGINES_TEXT.en);
  });
});

describe('CHAPTER_TRANSLATIONS', () => {
  it('covers all eight chapters in all three languages', () => {
    expect(Object.keys(CHAPTER_TRANSLATIONS)).toHaveLength(8);
    for (const [id, entry] of Object.entries(CHAPTER_TRANSLATIONS)) {
      for (const lang of LANGS) {
        expect(entry.title[lang], `${id}.title.${lang}`).toBeTruthy();
        expect(entry.summary[lang], `${id}.summary.${lang}`).toBeTruthy();
      }
    }
  });
});

describe('TEACHER_TEXT', () => {
  it('translates every workspace string into Hindi and Telugu', () => {
    for (const lang of NON_EN) {
      const script = lang === 'hi' ? /[ऀ-ॿ]/ : /[ఀ-౿]/;
      const copied = Object.entries(TEACHER_TEXT[lang])
        .filter(([, value]) => String(value).length > 3 && !script.test(String(value)))
        .map(([key]) => key);
      expect(copied, `untranslated ${lang} keys`).toEqual([]);
    }
  });

  it('keeps placeholders identical across languages', () => {
    for (const [key, value] of Object.entries(TEACHER_TEXT.en)) {
      const slots = String(value).match(/\{\w+\}/g) || [];
      for (const lang of NON_EN) {
        for (const slot of slots) {
          expect(String(TEACHER_TEXT[lang][key as keyof typeof TEACHER_TEXT.en]), `${lang}.${key}`).toContain(slot);
        }
      }
    }
  });

  it('names every route and misconception in all languages', () => {
    for (const table of [ROUTE_LABELS, MISCONCEPTION_LABELS]) {
      for (const [id, entry] of Object.entries(table)) {
        for (const lang of LANGS) {
          expect((entry as Record<string, string>)[lang], `${id}.${lang}`).toBeTruthy();
        }
      }
    }
  });
});
