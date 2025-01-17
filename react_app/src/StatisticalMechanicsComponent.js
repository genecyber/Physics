import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, Slider, Grid } from '@mui/material';

const StatisticalMechanicsComponent = () => {
  const [temperature, setTemperature] = useState(300); // Kelvin
  const [volume, setVolume] = useState(1.0); // m³
  const [particleCount, setParticleCount] = useState(6.022e23); // Avogadro's number
  const [pressure, setPressure] = useState(101325); // Pascal (1 atm)

  const handleTemperatureChange = (event, newValue) => {
    setTemperature(newValue);
    // Update pressure using ideal gas law: PV = NkT
    const k = 1.380649e-23; // Boltzmann constant
    setPressure((particleCount * k * newValue) / volume);
  };

  const handleVolumeChange = (event, newValue) => {
    setVolume(newValue);
    // Update pressure using ideal gas law
    const k = 1.380649e-23;
    setPressure((particleCount * k * temperature) / newValue);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          System Parameters
        </Typography>
        
        <Typography gutterBottom>
          Temperature (K)
        </Typography>
        <Slider
          value={temperature}
          onChange={handleTemperatureChange}
          min={0}
          max={1000}
          step={1}
          valueLabelDisplay="auto"
          sx={{ mb: 3 }}
        />

        <Typography gutterBottom>
          Volume (m³)
        </Typography>
        <Slider
          value={volume}
          onChange={handleVolumeChange}
          min={0.1}
          max={10}
          step={0.1}
          valueLabelDisplay="auto"
          sx={{ mb: 3 }}
        />

        <Typography variant="body1">
          Number of Particles: {particleCount.toExponential(3)}
        </Typography>
      </Paper>

      <Paper elevation={3} sx={{ p: 2 }}>
        <Typography variant="h6" align="center" gutterBottom>
          System Properties
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography variant="body1" align="center">
              Pressure: {(pressure / 101325).toFixed(3)} atm
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="body1" align="center">
              Average Energy: {(1.5 * 1.380649e-23 * temperature).toExponential(3)} J
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="body1" align="center">
              Entropy: {(particleCount * 1.380649e-23 * Math.log(volume)).toExponential(3)} J/K
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default StatisticalMechanicsComponent;
