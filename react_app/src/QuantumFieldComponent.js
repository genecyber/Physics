import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import { create, all } from 'mathjs';

const math = create(all);

function QuantumFieldComponent() {
  const [scalarField, setScalarField] = useState('exp(-(r^2)/(2*0.5^2)) * cos(5*r)'); // Gaussian wave packet
  const [fieldData, setFieldData] = useState(null);
  const [animation, setAnimation] = useState(null);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    // Cleanup animation on unmount
    return () => {
      if (animation) {
        clearInterval(animation);
      }
    };
  }, [animation]);

  const generateFieldData = (equation, t = 0) => {
    try {
      // Create a grid of x and y values
      const xValues = math.range(-5, 5, 0.2).toArray();
      const yValues = math.range(-5, 5, 0.2).toArray();
      
      // Calculate z values using the equation
      const zValues = [];
      for (let y of yValues) {
        const row = [];
        for (let x of xValues) {
          // Replace variables in the equation with actual values
          const scope = {
            x: x,
            y: y,
            t: t,
            r: math.sqrt(x*x + y*y),
            theta: math.atan2(y, x),
            pi: math.pi,
            e: math.e
          };
          
          try {
            const result = math.evaluate(equation, scope);
            row.push(result);
          } catch (e) {
            row.push(0);
          }
        }
        zValues.push(row);
      }

      return {
        x: xValues,
        y: yValues,
        z: zValues
      };
    } catch (e) {
      console.error('Error generating field data:', e);
      return null;
    }
  };

  const updateScalarField = () => {
    console.log('updateScalarField called with:', scalarField);
    fetch('http://localhost:5001/quantum_field/update_scalar_field', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ scalar_field: scalarField }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Response:', data);
      const newFieldData = generateFieldData(scalarField);
      if (newFieldData) {
        setFieldData(newFieldData);
      }
    })
    .catch(error => console.error('Error:', error));
  };

  const toggleAnimation = () => {
    if (isAnimating) {
      if (animation) {
        clearInterval(animation);
        setAnimation(null);
      }
    } else {
      let t = 0;
      const newAnimation = setInterval(() => {
        const newFieldData = generateFieldData(scalarField, t);
        if (newFieldData) {
          setFieldData(newFieldData);
        }
        t += 0.1;
      }, 50);
      setAnimation(newAnimation);
    }
    setIsAnimating(!isAnimating);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ marginBottom: '20px' }}>
        <input 
          type="text" 
          value={scalarField} 
          onChange={(e) => setScalarField(e.target.value)}
          placeholder="Enter scalar field equation (e.g., A*cos(k*r - w*t))"
          style={{ width: '400px', padding: '8px' }}
        />
        <button 
          onClick={updateScalarField}
          style={{
            marginLeft: '10px',
            padding: '8px 16px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Update Field
        </button>
        <button 
          onClick={toggleAnimation}
          style={{
            marginLeft: '10px',
            padding: '8px 16px',
            backgroundColor: isAnimating ? '#f44336' : '#2196F3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          {isAnimating ? 'Stop Animation' : 'Start Animation'}
        </button>
      </div>
      
      {fieldData && (
        <Plot
          data={[
            {
              type: 'surface',
              x: fieldData.x,
              y: fieldData.y,
              z: fieldData.z,
              colorscale: 'Viridis',
              contours: {
                z: {
                  show: true,
                  usecolormap: true,
                  highlightcolor: "#42f462",
                  project: { z: true }
                }
              }
            }
          ]}
          layout={{
            width: 800,
            height: 600,
            title: 'Quantum Field Visualization',
            scene: {
              xaxis: { title: 'x' },
              yaxis: { title: 'y' },
              zaxis: { title: 'Field Value' },
              camera: {
                eye: { x: 1.5, y: 1.5, z: 1.5 }
              }
            }
          }}
        />
      )}

      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <h3>Example Equations:</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li>Gaussian wave packet: exp(-(r^2)/(2*sigma^2)) * cos(k*r)</li>
          <li>Standing wave: sin(k*x) * cos(w*t)</li>
          <li>Traveling wave: cos(k*r - w*t)</li>
          <li>Quantum harmonic oscillator: exp(-r^2/2) * (1 - 2*r^2)</li>
        </ul>
      </div>
    </div>
  );
}

export default QuantumFieldComponent;
