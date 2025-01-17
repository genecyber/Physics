import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, Grid } from '@mui/material';

const ElectromagneticComponent = () => {
  // Default values represent a plane electromagnetic wave
  const [fieldTensor, setFieldTensor] = useState({
    E: { x: '0', y: 'cos(ωt - kz)', z: '0' },
    B: { x: '0', y: '0', z: 'cos(ωt - kz)' }
  });

  const handleFieldChange = (field, component, value) => {
    setFieldTensor(prev => ({
      ...prev,
      [field]: {
        ...prev[field],
        [component]: value
      }
    }));
  };

  const renderFieldInput = (field, component, label) => (
    <TextField
      label={label}
      value={fieldTensor[field][component]}
      onChange={(e) => handleFieldChange(field, component, e.target.value)}
      fullWidth
      margin="normal"
      size="small"
    />
  );

  return (
    <Box sx={{ p: 3 }}>
      <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          Electromagnetic Field Components
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom>
              Electric Field (E)
            </Typography>
            {renderFieldInput('E', 'x', 'Ex')}
            {renderFieldInput('E', 'y', 'Ey')}
            {renderFieldInput('E', 'z', 'Ez')}
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom>
              Magnetic Field (B)
            </Typography>
            {renderFieldInput('B', 'x', 'Bx')}
            {renderFieldInput('B', 'y', 'By')}
            {renderFieldInput('B', 'z', 'Bz')}
          </Grid>
        </Grid>

        <Box sx={{ mt: 2 }}>
          <Button variant="contained" color="primary">
            Visualize Fields
          </Button>
        </Box>
      </Paper>

      <Paper elevation={3} sx={{ p: 2 }}>
        <Typography variant="h6" align="center" gutterBottom>
          Field Properties
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography variant="body1" align="center">
              Energy Density: {'\u03B5\u2080E² + B²/\u03BC\u2080'}
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="body1" align="center">
              Poynting Vector: E × B
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="body1" align="center">
              Wave Type: Plane Wave
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default ElectromagneticComponent;
