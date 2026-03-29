import { Box, Typography, TextField, Button, Paper } from '@mui/material';

export default function IntakeForm() {
  return (
    <Box minHeight="100vh" display="flex" alignItems="center" justifyContent="center" bgcolor="background.default">
      <Paper elevation={6} sx={{ p: 5, maxWidth: 430, width: '100%', bgcolor: 'background.paper', borderRadius: 4 }}>
        <Typography variant="h5" color="primary" fontWeight={700} gutterBottom>
          Annual Income/Expenditure
        </Typography>
        <Box component="form" display="flex" flexDirection="column" gap={3} mt={2}>
          <TextField label="Age" name="age" type="number" required fullWidth color="primary" inputProps={{ min: 0 }} />
          <TextField label="BMI" name="bmi" type="number" required fullWidth color="primary" inputProps={{ min: 0, step: 0.1 }} />
          <TextField label="Children" name="children" type="number" required fullWidth color="primary" inputProps={{ min: 0 }} />
          <TextField label="Charges (Target)" name="charges" type="number" required fullWidth color="secondary" inputProps={{ min: 0 }} />
          <Button variant="contained" color="secondary" size="large" sx={{ mt: 1, fontWeight: 600 }} type="submit">
            Predict
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}