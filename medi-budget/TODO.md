# Medi-Budget INR Conversion Task

## Plan Steps:
- [ ] 1. Update backend/app.py: Multiply prediction by 83.5 (USD→INR), change currency to 'INR'
- [ ] 2. Update src/components/MedicalExpenseForm.jsx: 
  - Update mock prediction calculation * 83.5, currency: 'INR'
  - Update UI display: $ USD → ₹ INR
- [ ] 3. Test backend: cd backend && python app.py
- [ ] 4. Test frontend: cd .. && npm run dev
- [ ] 5. Verify predictions show INR (₹ symbol, ~83.5x larger values)
