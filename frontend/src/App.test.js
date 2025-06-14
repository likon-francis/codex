import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

test('renders portal title', () => {
  render(<App />);
  const title = screen.getByText(/Codex Document Analyzer/i);
  expect(title).toBeInTheDocument();
});

