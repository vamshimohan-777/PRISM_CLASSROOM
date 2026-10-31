import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('authentication experience', () => {
  it('presents a secure sign-in, CBSE framework, and hackathon demo personas', () => {
    render(<App />);
    expect(screen.getByText(/Misconception-aware learning/i)).toBeTruthy();
    expect(screen.getByText(/CBSE · CLASS VIII MATHEMATICS/i)).toBeTruthy();
    expect(screen.getByText(/Transparent Rules Engine/i)).toBeTruthy();
    expect(screen.getByText(/Aarav Sharma/i)).toBeTruthy();
    expect(screen.getByText(/Ms. Ananya/i)).toBeTruthy();
    expect(screen.getByRole('button', { name: /Sign in with credentials/i })).toBeTruthy();
    expect(screen.getByRole('button', { name: /Create account/i })).toBeTruthy();
  });
});
