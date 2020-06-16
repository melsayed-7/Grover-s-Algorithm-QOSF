from qiskit import *
from qiskit.circuit.library.standard_gates import XGate
from oracle import *
from diffuser import *
from utils import *
import math

#############################  ORACLE + DIFFUSER CIRCUIT  #############################
def grover_unit(list_values:list, circuit_type:str):
    
    n=len(list_values[0])
    
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    assert len(set(list_values)) == len(list_values), 'You should not have a duplicate string value in your list.'

    if (circuit_type == 'noancilla' or n==2):
        q1=QuantumRegister(n+1, "q")
        a1=QuantumCircuit(q1)
        a1.append(oracle(list_values, circuit_type), [*range(n+1)]) # Add oracle.
        a1.append(diffuser(list_values, circuit_type), [*range(n)]) # Add diffuser.
    
    elif circuit_type =='ancilla':
        q1=QuantumRegister(n*2, "q")
        a1=QuantumCircuit(q1)
        a1.append(oracle(list_values, circuit_type), [*range(n*2)])
        a1.append(diffuser(list_values, circuit_type), [*range(n*2)])
    
    return a1



#####################              GROVER'S CIRCUIT               ##################### 
def grover(list_values:list, circuit_type: str, prob_1 = 0, prob_2 = 0):

    n = len(list_values[0])
    N = len(list_values)
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    assert len(set(list_values)) == len(list_values), 'You should not have a duplicate string value in your list.'
    
    number_iterations = int((math.pi/4)*math.sqrt(math.pow(2,n)/N))

    circuit=initialize(list_values, circuit_type)

    ############### COMBINE: BALANCED STATE + ORACLE + DIFFUSER ###############
    # Iterate: (oracle+diffuser) + (oracle+diffuser) + ... .
    for i in range(number_iterations):
        circuit=circuit.combine(grover_unit(list_values, circuit_type))
    
    circuit.measure([*range(n)],[*range(n)]) # Measure the n qubits.

    noise_model, basis_gates = noise(prob_1, prob_2)

    return circuit, noise_model, basis_gates

