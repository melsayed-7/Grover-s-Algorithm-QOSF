from qiskit import *
from qiskit.circuit.library.standard_gates import XGate


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
