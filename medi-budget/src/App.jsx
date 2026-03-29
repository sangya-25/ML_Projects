import { CssBaseline } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MedicalExpenseForm from './components/MedicalExpenseForm';

function App() {
  return (
    <Router>
      <CssBaseline />
      <Routes>
        <Route path="/" element={<MedicalExpenseForm />} />
      </Routes>
    </Router>
  );
}

export default App;
