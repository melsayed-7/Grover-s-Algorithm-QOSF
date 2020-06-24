from qiskit import *
from qiskit.circuit.library.standard_gates import XGate


def oracle(list_values:list, circuit_type:str):
    n=len(list_values[0]) # Number of elements in one string.
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    
    if (circuit_type == 'noancilla' or n==2):
        q1=QuantumRegister(n+1, "q")
        a1=QuantumCircuit(q1)
        ##a1.barrier()
        for element in list_values:
            ############ If an element in string equal 0 then apply X Gate on the left of the control dot. 
            for i in range(n):
                if element[::-1][i] == '0':
                    a1.x(q1[i])
            ############
            # Apply n-1 qubits control Toffoli gate.
            gate = XGate().control(n)
            a1.append(gate, q1)
            ############ If an element in string equal 0 then apply X Gate on the right of the control dot. 
            for i in range(n):
                if element[::-1][i] == '0':
                    a1.x(q1[i])
            ############
            ##a1.barrier()
        
    elif circuit_type=='ancilla':
        r = 0
        pn = r + 2
        jn = r
        kn= r+1

        q1=QuantumRegister(n*2, "q")
        a1=QuantumCircuit(q1)
        ##a1.barrier()

        for element in list_values:
            ############
            for i in range(n):
                if element[::-1][i] == '0':
                    a1.x(q1[i])
            
            ############
            # Apply n-1 qubits control Toffoli gate using 2-qubits control Toffoli gates.
            a1.ccx(q1[r],q1[r+1],q1[r+n])
            for i in range(n-2):
                a1.ccx(q1[pn],q1[n+jn],q1[n+kn])
                if i<n-3:
                    pn+=1
                    jn+=1
                    kn+=1
            a1.cx(q1[(n*2)-2], q1[(n*2)-1])
    
            for i in range(n-2):
                a1.ccx(q1[pn],q1[n+jn],q1[n+kn])
                if i<n-3:
                    pn+=-1
                    jn+=-1
                    kn+=-1
            a1.ccx(q1[r],q1[r+1],q1[r+n])

            ############
            for i in range(n):
                if element[::-1][i] == '0':
                    a1.x(q1[i])
            ############

            ##a1.barrier()
            
    return a1
