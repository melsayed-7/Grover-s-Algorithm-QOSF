#!/usr/bin/env python
# coding: utf-8

# In[2]:


from qiskit import *
from qiskit.circuit.library.standard_gates import XGate

def grover_itera(t1:str, circuit_type: str, number_iteration: int):
    
    '''Summary:
        This code is general, accepts  as input any string of a binary number to be searched for.
        He can only search for one solution at the moment.
        
        The boolean oracle and diffuser operator are implemented in two different way:

            1- An 'ancilla' circuit; this way of implementing the circuit, regardless of other gates, uses
            two-control Toffoli gates, thus the oracle and the diffuser must rely on the ancillary qubits 
            to be used.

            2- An 'noancilla' circuit, uses multiple-control Toffoli gates instead of two-control Toffoli 
            gates in both oracle and diffuser parts. Thus, less qubit will be used but the depth of the
            circuit will increase.

        We may see the difference between those circuits by evaluating the quantum cost of the circuit.
        
        Arguments:
        The below code take as an input:

            - t1: a string of binary number.
            
            - circuit_type: 'ancilla' or 'noancilla'.
            
            - number_iteration: the number of Grover's iteration. 
              This is determined as $\frac{\pi}{4} \sqrt{2^n}$ n is the lenght of the string = 
              the number of qubits.
              For inctance number_iteration=2 →(oracle+diffuser)+(oracle+diffuser).
              
        Returns:
        Output the Grover's circuit.'''

    n=len(t1)
    
############################   ORACLE   ###############################

    def oracle(t1:str, circuit_type: str):
        
        if n<2 :
            raise ValueError('Lenght of input should be greater or equal to 2') 
        else:
                    
            if (circuit_type == 'noancilla' or n==2):
                q1=QuantumRegister(n+1, "q")
                a1=QuantumCircuit(q1)
                ############
                for i in range(n):
                    if t1[::-1][i] == '0':
                        a1.x(q1[i])
                ############
                gate = XGate().control(n)
                a1.append(gate, q1)
                
            elif circuit_type=='ancilla':
                r,pn,jn,kn=0,2,0,1
                q1=QuantumRegister(n*2, "q")
                a1=QuantumCircuit(q1)
                ############
                for i in range(n):
                    if t1[::-1][i] == '0':
                        a1.x(q1[i])
                ############
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
            if t1[::-1][i] == '0':
                a1.x(q1[i])
        ############
        return a1

##############################  GROVER'S DIFFUSER  #############################
    def diffuser(t1: str, circuit_type:str):
        if len(t1) < 2:
            raise ValueError('Lenght of input should be greater or equal to 2')
        else:
            if (circuit_type=='noancilla' or n==2):

                q1=QuantumRegister(n, "q")
                a1=QuantumCircuit(q1)
        
                a1.h(q1[[*range(n)]])
                a1.x(q1[[*range(n)]])
                a1.h(q1[n-1])
                
                gate = XGate().control(n-1)
                a1.append(gate, q1)
            
            elif circuit_type=='ancilla':
                r,pn,jn,kn=0,2,0,1
                q1=QuantumRegister(n*2, "q")
                a1=QuantumCircuit(q1)
            
                #########
                a1.h(q1[[*range(n)]])
                a1.x(q1[[*range(n)]])
                a1.h(q1[n-1])
                a1.barrier()
                #########
        
                a1.ccx(q1[r],q1[r+1],q1[r+n])
                for i in range(n-3):
                    a1.ccx(q1[pn],q1[n+jn],q1[n+kn])
                    if i<n-4:
                        pn+=1
                        jn+=1
                        kn+=1
                
                a1.barrier()
                
                a1.cx(q1[(n*2)-3], q1[(n-1)])
                a1.barrier()
        
                for i in range(n-3):
                    a1.ccx(q1[pn],q1[n+jn],q1[n+kn])
                    if i<n-4:
                        pn+=-1
                        jn+=-1
                        kn+=-1
                a1.ccx(q1[r],q1[r+1],q1[r+n])
                
            
        a1.h(q1[n-1])
        a1.x(q1[[*range(n)]])
        a1.h(q1[[*range(n)]])
        return a1
#############################  ORACLE + DIFFUSER CIRCUIT  #############################
    def grover(t1: str, circuit_type: str):
        
        if (circuit_type == 'noancilla' or n==2):
            q1=QuantumRegister(n+1, "q")
            a1=QuantumCircuit(q1)
            a1.append(oracle(t1, circuit_type), [*range(n+1)])
            a1.append(diffuser(t1, circuit_type), [*range(n)])
        elif circuit_type =='ancilla':
            q1=QuantumRegister(n*2, "q")
            a1=QuantumCircuit(q1)
            a1.append(oracle(t1, circuit_type), [*range(n*2)])
            a1.append(diffuser(t1, circuit_type), [*range(n*2)])
        return a1
    
#####################  INITIALIZE THE CIRCUIT WITH BALANCED STATE  #####################
    def initialize(t1:str, circuit_type:str):
        
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
    
    circuit=initialize(t1, circuit_type)
    
##################### COMBINE: BALANCED STATE + ORACLE + DIFFUSER #####################
    
    for i in range(number_iteration):
        circuit=circuit.combine(grover(t1, circuit_type))
        
    circuit.measure([*range(n)],[*range(n)])
    
    return circuit

