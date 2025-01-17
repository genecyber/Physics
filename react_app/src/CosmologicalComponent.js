import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, Slider } from '@mui/material';

const CosmologicalComponent = () => {
  const [density, setDensity] = useState(0.3); // Critical density ratio (Omega)
  const [hubbleConstant, setHubbleConstant] = useState(67.4); // km/s/Mpc
  const [darkEnergy, setDarkEnergy] = useState(0.7); // Dark energy density parameter

  const handleDensityChange = (event, newValue) => {
    setDensity(newValue);
  };

  const handleHubbleChange = (event, newValue) => {
    setHubbleConstant(newValue);
  };

  const handleDarkEnergyChange = (event, newValue) => {
    setDarkEnergy(newValue);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          Universe Parameters
        </Typography>
        
        <Typography gutterBottom>
          Matter Density (Ωm)
        </Typography>
        <Slider
          value={density}
          onChange={handleDensityChange}
          min={0}
          max={1}
          step={0.01}
          valueLabelDisplay="auto"
          sx={{ mb: 3 }}
        />

        <Typography gutterBottom>
          Hubble Constant (H₀)
        </Typography>
        <Slider
          value={hubbleConstant}
          onChange={handleHubbleChange}
          min={50}
          max={100}
          step={0.1}
          valueLabelDisplay="auto"
          sx={{ mb: 3 }}
        />

        <Typography gutterBottom>
          Dark Energy Density (ΩΛ)
        </Typography>
        <Slider
          value={darkEnergy}
          onChange={handleDarkEnergyChange}
          min={0}
          max={1}
          step={0.01}
          valueLabelDisplay="auto"
        />
      </Paper>

      <Paper elevation={3} sx={{ p: 2 }}>
        <Typography variant="h6" align="center" gutterBottom>
          Universe Evolution
        </Typography>
        <Typography variant="body1" align="center">
          Current Age: {((1 / hubbleConstant) * 13.8).toFixed(1)} billion years
        </Typography>
        <Typography variant="body1" align="center">
          Fate: {density + darkEnergy > 1 ? 'Big Crunch' : density + darkEnergy < 1 ? 'Heat Death' : 'Critical Balance'}
        </Typography>
      </Paper>
    </Box>
  );
};

export default CosmologicalComponent;
