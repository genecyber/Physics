import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the enhanced simulation function for Copper with variations and stability checks
def simulate_superconductivity_copper(B_func, E_func, simulation_time=50, time_steps=500):
    def equations_of_motion(t, y):
        B = B_func(t)
        E = E_func(t)
        psi, phi, chi, eta = y
        
        lorentz_force = -1 * 1 * B * psi
        electric_interaction = -1 * E * psi
        coherence_gain = B * E * np.abs(psi)
        
        # Add stability checks
        d_psi_dt = np.clip(-1.0 * psi + phi * chi + lorentz_force + electric_interaction, -1e10, 1e10)
        d_phi_dt = np.clip(-0.5 * phi, -1e10, 1e10)
        d_chi_dt = np.clip(-psi * phi, -1e10, 1e10)
        d_eta_dt = np.clip(coherence_gain - eta, -1e10, 1e10)
        
        return [d_psi_dt, d_phi_dt, d_chi_dt, d_eta_dt]
    
    y0 = [0.1, 0.1, 0.1, 0.0]
    t_span = (0, simulation_time)
    t_eval = np.linspace(0, simulation_time, time_steps)
    
    sol = solve_ivp(equations_of_motion, t_span, y0, method='RK45', t_eval=t_eval)
    
    coherence = np.max(sol.y[3])
    return coherence, sol

# Define random parameter functions
def random_pulsed_field(t, amplitude, period):
    return amplitude if (t % period) < (period / 2) else 0

# Number of simulations
num_simulations = 20

# Simulation results
results = []

for _ in range(num_simulations):
    # Randomize parameters
    B_amplitude = np.random.uniform(0.64, 0.96)  # 0.8 ± 20%
    E_amplitude = np.random.uniform(640, 960)  # 800 ± 20%
    period = np.random.uniform(5, 15)  # 10 ± 50%
    frequency = np.random.uniform(0.05, 0.15)  # 0.1 ± 50%
    
    # Pulsed fields with random parameters
    B_pulse_func = lambda t: random_pulsed_field(t, B_amplitude, period)
    E_pulse_func = lambda t: random_pulsed_field(t, E_amplitude, period)
    
    # Run simulation
    coherence, sol = simulate_superconductivity_copper(B_pulse_func, E_pulse_func)
    results.append((B_amplitude, E_amplitude, period, frequency, coherence, sol))

# Plot the results
plt.figure(figsize=(12, 6))
for i, (B, E, period, freq, coherence, sol) in enumerate(results):
    plt.plot(sol.t, sol.y[3], label=f'Sim {i+1} (Coh={coherence:.4f})')
plt.xlabel('Time')
plt.ylabel('Coherence Level')
plt.title('Superconducting Coherence Over Time for Copper with Randomized Parameters')
plt.legend()
plt.show()

# Display the best result
best_result = max(results, key=lambda x: x[4])
best_params = best_result[:4]
best_coherence = best_result[4]

best_params, best_coherence
