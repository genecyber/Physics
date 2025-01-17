import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Line2 } from 'three/examples/jsm/lines/Line2';
import { LineMaterial } from 'three/examples/jsm/lines/LineMaterial';
import { LineGeometry } from 'three/examples/jsm/lines/LineGeometry';

function GeneralRelativityComponent() {
  const [metricTensor, setMetricTensor] = useState('-1,0,0,0;0,1,0,0;0,0,r^2,0;0,0,0,r^2*sin^2(θ)'); // Schwarzschild metric
  const [spacetimeCurvature, setSpacetimeCurvature] = useState(null);
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const cameraRef = useRef(null);
  const controlsRef = useRef(null);

  useEffect(() => {
    console.log('GeneralRelativityComponent mounted');
    initScene();
    return () => cleanupScene();
  }, []);

  useEffect(() => {
    if (spacetimeCurvature) {
      updateVisualization();
    }
  }, [spacetimeCurvature]);

  const initScene = () => {
    // Create scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    sceneRef.current = scene;

    // Create camera
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(5, 5, 5);
    cameraRef.current = camera;

    // Create renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth / 2, window.innerHeight / 2);
    mountRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Add controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controlsRef.current = controls;

    // Add grid
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    // Start animation loop
    animate();
  };

  const animate = () => {
    if (!mountRef.current) return;
    
    requestAnimationFrame(animate);
    if (controlsRef.current) controlsRef.current.update();
    if (rendererRef.current && sceneRef.current && cameraRef.current) {
      rendererRef.current.render(sceneRef.current, cameraRef.current);
    }
  };

  const cleanupScene = () => {
    if (mountRef.current && rendererRef.current) {
      mountRef.current.removeChild(rendererRef.current.domElement);
    }
  };

  const updateVisualization = () => {
    if (!sceneRef.current) return;

    // Remove old visualization
    const oldCurve = sceneRef.current.getObjectByName('spacetimeCurve');
    if (oldCurve) sceneRef.current.remove(oldCurve);

    // Create new visualization based on spacetimeCurvature
    const points = [];
    const resolution = 50;
    for (let i = 0; i < resolution; i++) {
      for (let j = 0; j < resolution; j++) {
        const x = (i - resolution/2) * 0.2;
        const z = (j - resolution/2) * 0.2;
        const y = spacetimeCurvature * Math.exp(-(x*x + z*z));
        points.push(x, y, z);
      }
    }

    const geometry = new LineGeometry();
    geometry.setPositions(points);

    const material = new LineMaterial({
      color: 0x00ff00,
      linewidth: 2,
    });

    const curve = new Line2(geometry, material);
    curve.name = 'spacetimeCurve';
    curve.computeLineDistances();
    sceneRef.current.add(curve);
  };

  const updateMetricTensor = () => {
    console.log('updateMetricTensor called with:', metricTensor);
    fetch('http://localhost:5001/general_relativity/update_metric_tensor', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ metric_tensor: metricTensor }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Response:', data);
      // Calculate spacetime curvature from metric tensor
      const curvature = calculateCurvature(metricTensor);
      setSpacetimeCurvature(curvature);
    })
    .catch(error => console.error('Error:', error));
  };

  const calculateCurvature = (metricTensor) => {
    // Parse the metric tensor string and calculate Ricci curvature
    // This is a simplified calculation for visualization purposes
    try {
      const components = metricTensor.split(';').map(row => 
        row.split(',').map(val => parseFloat(val) || 0)
      );
      // Calculate a simple scalar curvature value
      return components.reduce((sum, row) => 
        sum + row.reduce((rowSum, val) => rowSum + Math.abs(val), 0), 0
      ) / (components.length * components[0].length);
    } catch (e) {
      console.error('Error calculating curvature:', e);
      return 1.0; // Default curvature
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ marginBottom: '20px' }}>
        <input 
          type="text" 
          value={metricTensor} 
          onChange={(e) => setMetricTensor(e.target.value)}
          placeholder="Enter metric tensor (format: g00,g01,g02,g03;g10,g11,g12,g13;...)"
          style={{ width: '400px', padding: '8px' }}
        />
        <button 
          onClick={updateMetricTensor}
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
          Update Metric Tensor
        </button>
      </div>
      <div ref={mountRef} style={{ border: '1px solid #ccc', borderRadius: '4px' }} />
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <h3>Spacetime Curvature Visualization</h3>
        <p>Current curvature scalar: {spacetimeCurvature?.toFixed(4) || 'Not calculated'}</p>
      </div>
    </div>
  );
}

export default GeneralRelativityComponent;
