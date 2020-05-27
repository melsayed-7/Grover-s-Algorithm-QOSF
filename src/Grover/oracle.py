import qiskit

def oracle(circuit, gates_count):
    """[summary]
    This an oracle function that can be later implemented as a class
    It applies specific operations on a given quantum circuit

    Arguments:
        circuit {[qiskit.Quantum Circuit]} -- The circuit that we will apply
        the oracle on.

        gates_count {[int]} -- gates_count variable to be updated

    Returns:
        [circuit] -- [description]
    """

    assert circuit.n_qubits >= 8, 'This oracle works on 8 qubits'

    circuit.barrier()

    circuit.x([1,2,5,7])
    gates_count += 4  # in a more modular way the count of 0 in the target string
    

    nbit_toffoli_gate(circuit, 8, gates_count)
    circuit.x([1,2,5,7])
    gates_count += 4 
    circuit.barrier()

    



def nbit_toffoli_gate(circuit, N, gates_count):
    """[summary]
    This function applies N-bit toffoli on a given Circuit

    Arguments:
        N {int} -- number of qubits used in the toffoli gate
        circuit {qiskit.Quantum Circuit} -- The quantum circuit used
        gates_count {int} -- 
    """
    assert circuit.n_qubits >= 2*N, 'The circuit is not big enough to apply {}-toffoli gate'.format(N)
        
    circuit.ccx(0,1,N)
    gates_count += 1 

    for x in range(2,N):
        y = x+N-2
        z = x+N-1
        circuit.ccx(x,y,z)
        gates_count += 1
    
    circuit.cx(2*N-2,2*N-1)
    gates_count += 1
    
    for x in range(7,1,-1):
        y = N+x-2
        z = N+x-1
        circuit.ccx(x,y,z)
        gates_count += 1

    circuit.ccx(0,1,N)
    gates_count += 1

