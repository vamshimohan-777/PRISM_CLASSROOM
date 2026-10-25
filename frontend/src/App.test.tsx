import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('entry experience', () => {
  it('explains the adaptive learning loop and offers both roles', () => {
    render(<App />);
    expect(screen.getByText(/Every fraction answer/i)).toBeTruthy();
    expect(screen.getByRole('button', { name: /Enter student demo/i })).toBeTruthy();
    expect(screen.getByRole('button', { name: /Open teacher dashboard/i })).toBeTruthy();
  });
});
