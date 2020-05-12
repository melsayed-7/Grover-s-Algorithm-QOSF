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
    circuit.ccx(0,1,8)
    x=2
    y=8
    z=9
    while x<8:
        circuit.ccx(x,y,z)
        x=x+1
        y=y+1
        z=z+1
    circuit.cx(14,15)
    while x>2:
        x=x-1
        y=y-1
        z=z-1
        circuit.ccx(x,y,z)
    circuit.ccx(0,1,8)
    circuit.x([1,2,5,7])
    circuit.barrier()
    return circuit
    
