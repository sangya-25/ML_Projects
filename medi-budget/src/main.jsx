import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import './index.css';
import App from './App.jsx';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#b16eff' },
    secondary: { main: '#d72660' },
    background: { default: '#181028', paper: '#20123a' },
    text: { primary: '#faf7ff' },
  },
  shape: { borderRadius: 16 },
  typography: { fontFamily: 'Inter, system-ui, sans-serif' },
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </StrictMode>
);
