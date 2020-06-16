from qiskit import *
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, thermal_relaxation_error, depolarizing_error




def initialize(list_values:list, circuit_type:str):
    n=len(list_values[0])

    if (circuit_type == 'noancilla' or n==2): 
        q=QuantumRegister(n+1, "q")
        c=ClassicalRegister(n, "c")
        a=QuantumCircuit(q,c)
        a.x(q[n])
        a.h(q[[*range(n+1)]])
         
    elif circuit_type =='ancilla':
        q=QuantumRegister(n*2, "q")
        c=ClassicalRegister(n, "c")
        a=QuantumCircuit(q,c)
        a.x(q[n*2-1])
        a.h(q[n*2-1])
        a.h(q[[*range(n)]])
    return a


def noise(prob_1 = 0.0, prob_2 = 0.0):
    # Depolarizing quantum errors
    error_1 = depolarizing_error(prob_1, 1)
    error_2 = depolarizing_error(prob_2, 2)

    # Add errors to noise model
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_1, ['u1', 'u2', 'u3'])
    noise_model.add_all_qubit_quantum_error(error_2, ['cx'])

    # Get basis gates from noise model
    basis_gates = noise_model.basis_gates

    return noise_model, basis_gates
