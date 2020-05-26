import qiskit

def oracle(circuit):
    """[summary]
    This an oracle function that can be later implemented as a class
    It applies specific operations on a given quantum circuit

    Arguments:
        circuit {[qiskit.Quantum Circuit]} -- The circuit that we will apply
        the oracle on.

    Returns:
        [circuit] -- [description]
    """

    assert circuit.n_qubits >= 8, 'This oracle works on 8 qubits'

    circuit.barrier()

    circuit.x([1,2,5,7])
    circuit = nbit_toffoli_gate(circuit, 8)
    circuit.x([1,2,5,7])
    
    circuit.barrier()

    return circuit
    



def nbit_toffoli_gate(circuit, N):
    """[summary]
    This function applies N-bit toffoli on a given Circuit

    Arguments:
        N {[int]} -- number of qubits used in the toffoli gate
        circuit {qiskit.Quantum Circuit}] -- The quantum circuit used
    """
    assert circuit.n_qubits >= 2*N, 'The circuit is not big enough to apply {}-toffoli gate'.format(N)
        
    circuit.ccx(0,1,N)
    
    for x in range(2,N):
        y = x+N-2
        z = x+N-1
        circuit.ccx(x,y,z)
    
    circuit.cx(2*N-2,2*N-1)
    
    for x in range(7,1,-1):
        y = N+x-2
        z = N+x-1
        circuit.ccx(x,y,z)

    circuit.ccx(0,1,N)

    return circuit
