#!/usr/bin/env python
# coding: utf-8

# In[2]:


from qiskit import *
from qiskit.circuit.library.standard_gates import ZGate
############################   ORACLE   ###############################
def phase_oracle(list_values:list, circuit_type:str):
    n=len(list_values[0]) # Number of elements in one string.
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    
    if (circuit_type == 'noancilla' or n==2):
        q1=QuantumRegister(n, "q")
        a1=QuantumCircuit(q1)
        #a1.barrier()
        for element in list_values:
            ############ If an element in string equal 0 then apply X Gate on the left of the control dot. 
            for i in range(n):
                if element[::-1][i] == '0':
                    a1.x(q1[i])
            ############
            # Apply n-1 qubits control Toffoli gate.
            gate = ZGate().control(n-1)
            a1.append(gate, q1)
            ############ If an element in string equal 0 then apply X Gate on the right of the control dot. 
            for i in range(n):
                if element[::-1][i] == '0':
                    a1.x(q1[i])
            ############
            #a1.barrier()
        
    elif circuit_type=='ancilla':
        if n==3:
            q1=QuantumRegister(4, "q")
            a1=QuantumCircuit(q1)
            for element in list_values:
                ############
                for i in range(n):
                    if element[::-1][i] == '0':
                        a1.x(q1[i])
                ############
                a1.ccx(0,1,3)
                a1.cz(3,2)
                a1.ccx(0,1,3)
                ############
                for i in range(n):
                    if element[::-1][i] == '0':
                        a1.x(q1[i])
                ############
        else:
            pn,jn,kn=2,0,1
            q1=QuantumRegister(n+(n-3), "q")
            a1=QuantumCircuit(q1)
            #a1.barrier()
            for element in list_values:
                ############
                for i in range(n):
                    if element[::-1][i] == '0':
                        a1.x(q1[i])
                ############
                # Apply n-1 qubits control Toffoli gate using 2-qubits control Toffoli gates.
                a1.ccx(q1[0],q1[1],q1[n])
                for i in range(n-4):
                    a1.ccx(q1[pn],q1[n+jn],q1[n+kn])
                    if i<n-5:
                        pn+=1
                        jn+=1
                        kn+=1
                #a1.barrier()
                a1.h(q1[n-1])
                a1.ccx(q1[(n-2)], q1[n+(n-4)], q1[n-1])
                a1.h(q1[n-1])
                #a1.barrier()
                
                for i in range(n-4):
                    a1.ccx(q1[pn],q1[n+jn],q1[n+kn])
                    if i<n-5:
                        pn+=-1
                        jn+=-1
                        kn+=-1
                a1.ccx(q1[0],q1[1],q1[n])
                ############
                for i in range(n):
                    if element[::-1][i] == '0':
                        a1.x(q1[i])
                ############
                #a1.barrier()
    return a1
##############################  GROVER'S DIFFUSER  #############################
def phase_diffuser(list_values:list, circuit_type:str):
    import numpy as np
    n=len(list_values[0])
    assert n>=2, 'Length of input should be greater or equal to 2.'
    
    if (circuit_type=='noancilla' or n==2):
        q1=QuantumRegister(n, "q")
        a1=QuantumCircuit(q1)
        a1.rx(np.pi/2, q1[[*range(n)]])
        a1=a1.combine(phase_oracle(['1'*n], 'noancilla'))
        a1.rx(-np.pi/2, q1[[*range(n)]])
    
    elif circuit_type=='ancilla':
        if n==3:
            q1=QuantumRegister(4, "q")
            a1=QuantumCircuit(q1)
            a1.rx(np.pi/2, q1[[*range(n)]])
            a1=a1.combine(phase_oracle(['1'*n], 'ancilla'))
            a1.rx(-np.pi/2, q1[[*range(n)]])
            
        else:
            
            q1=QuantumRegister(n+(n-3), "q")
            a1=QuantumCircuit(q1)
            a1.rx(np.pi/2, q1[[*range(n)]])
            a1=a1.combine(phase_oracle(['1'*n], 'ancilla'))
            a1.rx(-np.pi/2, q1[[*range(n)]])
    return a1
############################# AA= ORACLE + DIFFUSER CIRCUIT  #############################
def phase_amplitude_amplification(list_values:list, circuit_type:str):
    n=len(list_values[0])
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    assert len(set(list_values)) == len(list_values), 'You should not have a duplicate string value in your list.'

    if (circuit_type == 'noancilla' or n==2):
        a1=phase_oracle(list_values, circuit_type) # Add oracle.
        a1=a1.combine(phase_diffuser(list_values, circuit_type)) # Add diffuser.
    elif circuit_type =='ancilla':
        if n==3:
            a1=phase_oracle(list_values, circuit_type)
            a1=a1.combine(phase_diffuser(list_values, circuit_type))
        else:
            a1=phase_oracle(list_values, circuit_type)
            a1=a1.combine(phase_diffuser(list_values, circuit_type))
    return a1
#####################  PREPARE THE CIRCUIT WITH BALANCED STATE  #####################
def preparation(list_values:list, circuit_type:str):
    import numpy as np
    n=len(list_values[0])

    if (circuit_type == 'noancilla' or n==2): 
        q=QuantumRegister(n, "q")
        c=ClassicalRegister(n, "c")
        a=QuantumCircuit(q,c)
        a.rx(np.pi/2 ,q[[*range(n)]])
         
    elif circuit_type =='ancilla':
        if n==3:
            q=QuantumRegister(4, "q")
        else:
            q=QuantumRegister(n+(n-3), "q")
        c=ClassicalRegister(n, "c")
        a=QuantumCircuit(q,c)
        a.rx(np.pi/2 ,q[[*range(n)]])

    return a
#####################              GROVER'S CIRCUIT               #####################
def phase_grover(list_values:list, circuit_type: str, number_iterations: int):
    n=len(list_values[0])
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    assert len(set(list_values)) == len(list_values), 'You should not have a duplicate string value in your list.'
    
    circuit=preparation(list_values, circuit_type)

        ############### COMBINE: BALANCED STATE + ORACLE + DIFFUSER ###############
    # Iterate: (oracle+diffuser) + (oracle+diffuser) + ... .
    for i in range(number_iterations):
        circuit=circuit.combine(phase_amplitude_amplification(list_values, circuit_type))
    
    circuit.measure([*range(n)],[*range(n)]) # Measure the n qubits.

    return circuit

