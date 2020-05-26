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
    #string to be found is 01011001
    circuit=QuantumCircuit(16,8)
    a=[0,1,2,3,4,5,6,7,15]
    b=[0,1,2,3,4,5,6,7]
    circuit.x(15)
    circuit.h(a)
    for i in range(12):
        
        #oracle
        circuit = oracle(circuit)

        #grover diffusion operator
        circuit.barrier()
        circuit.h(b)
        circuit.x(b)
        circuit = nbit_toffoli_gate(circuit, 8)
        circuit.x(b)
        circuit.h(b)


    circuit.barrier()
    circuit.barrier()  
    circuit.measure(b,b)
    simulator=Aer.get_backend('qasm_simulator')
    result=execute(circuit,simulator).result()
    measurement=result.get_counts()
    print(measurement)

    return measurement

search(1,1,oracle)



    


