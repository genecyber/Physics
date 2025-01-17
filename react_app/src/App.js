import React, { useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import GeneralRelativityComponent from './GeneralRelativityComponent';
import QuantumFieldComponent from './QuantumFieldComponent';
import CosmologicalComponent from './CosmologicalComponent';
import ElectromagneticComponent from './ElectromagneticComponent';
import StatisticalMechanicsComponent from './StatisticalMechanicsComponent';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
    background: {
      default: '#0a1929',
      paper: '#1e1e1e',
    },
  },
});

function App() {
  useEffect(() => {
    console.log('App component mounted');
  }, []);

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Container maxWidth="xl">
        <Box sx={{ py: 4 }}>
          <Typography variant="h2" component="h1" gutterBottom align="center" sx={{ mb: 6 }}>
            Unified Theory Dashboard
          </Typography>
          
          <Box sx={{ mb: 4 }}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h4" component="h2" gutterBottom>
                General Relativity
              </Typography>
              <GeneralRelativityComponent />
            </Paper>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h4" component="h2" gutterBottom>
                Quantum Field Theory
              </Typography>
              <QuantumFieldComponent />
            </Paper>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h4" component="h2" gutterBottom>
                Cosmology
              </Typography>
              <CosmologicalComponent />
            </Paper>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h4" component="h2" gutterBottom>
                Electromagnetism
              </Typography>
              <ElectromagneticComponent />
            </Paper>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h4" component="h2" gutterBottom>
                Statistical Mechanics
              </Typography>
              <StatisticalMechanicsComponent />
            </Paper>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;