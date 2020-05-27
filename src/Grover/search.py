from qiskit import *
from math import * # use np instead
from qiskit.tools.visualization import plot_histogram
import numpy as np
from oracle import *

def search(to_be_searched, target, oracle):
    """[summary]
        This is a search function that, for now, has a predefined circuit for testing.

    Arguments:
        to_be_searched {[list of elements]} -- This is a pointer to the list we need to search inside
        target {n_bits} -- n_bit representation of the target element
        oracle {[function]} -- This function takes the circuit and apply the orcale

    Returns:
        [int] -- position of the target key in the array
    """

    gates_count = 0
    #string to be found is 01011001
    circuit=QuantumCircuit(16,8)
    a=[0,1,2,3,4,5,6,7,15]
    b=[0,1,2,3,4,5,6,7]
    
    circuit.x(15)
    gates_count += 1

    circuit.h(a)
    gates_count += len(a)

    for i in range(12):
        #oracle
        # circuit = 
        oracle(circuit, gates_count)

        #grover diffusion operator
        circuit.barrier()
        circuit.h(b)
        circuit.x(b)
        gates_count += 2

        nbit_toffoli_gate(circuit, 8, gates_count)
        
        circuit.x(b)
        circuit.h(b)
        gates_count += 2


    circuit.barrier()
    circuit.barrier()  
    circuit.measure(b,b)
    simulator=Aer.get_backend('qasm_simulator')
    result=execute(circuit,simulator).result()
    measurement=result.get_counts()
    print(measurement)
    print(gates_count)

    return measurement

search(1,1,oracle)



    


