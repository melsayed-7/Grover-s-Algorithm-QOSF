from qiskit import *
from qiskit.circuit.library.standard_gates import XGate


def diffuser(list_values:list, circuit_type:str):
    n=len(list_values[0])
    assert n>=2, 'Length of input should be greater or equal to 2.'
    
    if (circuit_type=='noancilla' or n==2):

        q1=QuantumRegister(n, "q")
        a1=QuantumCircuit(q1)

        a1.h(q1[[*range(n)]])
        a1.x(q1[[*range(n)]])
        a1.h(q1[n-1])
        
        gate = XGate().control(n-1)
        a1.append(gate, q1)
    
    elif circuit_type=='ancilla':
        r = 0
        pn = r + 2
        jn = r
        kn= r+1
        q1=QuantumRegister(n*2, "q")
        a1=QuantumCircuit(q1)
    
        ######### Apply Hadamard and X gates.
        a1.h(q1[[*range(n)]])
        a1.x(q1[[*range(n)]])
        a1.h(q1[n-1]) # Apply Hadamrd gate on the left of the target qubit n.
        #########

        a1.ccx(q1[r],q1[r+1],q1[r+n])
        for i in range(n-3):
            a1.ccx(q1[pn],q1[n+jn],q1[n+kn])
            if i<n-4:
                pn+=1
                jn+=1
                kn+=1
        
        ##a1.barrier()
        a1.cx(q1[(n*2)-3], q1[(n-1)])
        ##a1.barrier()

        for i in range(n-3):
            a1.ccx(q1[pn],q1[n+jn],q1[n+kn])
            if i<n-4:
                pn+=-1
                jn+=-1
                kn+=-1
        a1.ccx(q1[r],q1[r+1],q1[r+n])

    ######### Apply Hadamard and X gates.
    a1.h(q1[n-1]) # Apply Hadamrd gate on the right of the target qubit n.
    a1.x(q1[[*range(n)]])
    a1.h(q1[[*range(n)]])
    #########
    return a1
