from qiskit import *
from qiskit.circuit.library.standard_gates import XGate

'''Summary:
    This code is general, accepts  as input any string of binary numbers to be searched for,
    and he can search for multiple solutions.
    
    The boolean oracle and diffuser operator are implemented in two different way:
        1- An 'ancilla' circuit: this way of implementing the circuit, regardless of other gates, uses
        two-control Toffoli gates, thus the oracle and the diffuser must rely on the ancillary qubits 
        to be used.
        2- An 'noancilla' circuit: uses multiple-control Toffoli gates instead of two-control Toffoli 
        gates in both oracle and diffuser parts. Thus, less qubit will be used but the depth of the
        circuit will increase.
    We may see the difference between those circuits by evaluating the quantum cost of the circuit.
    
    Arguments:
    The below code take as an input:
        - list_values: a list of the values to be searched which contains strings of unique binary
        numbers, for instance: ['111', '001', '000', ...].
        
        - circuit_type: 'ancilla' or 'noancilla'.
        
        - number_iterations: the number of Grover's iteration, this is determined as: 
            --For the case of one solution: $\frac{\pi}{4} \sqrt{2^n}$ n is the lenght of the string = 
            the number of qubits.
            --For the case of m solution: $\frac{\pi}{4} \sqrt{\frac{2^n}{m}}$ where m is the number of
            the solutions.
            For inctance, number_iterations=2 →(oracle+diffuser)+(oracle+diffuser).
            
    Returns:
    Output the Grover's circuit; this is returned by the last function in this code `grover_itera()`.'''

############################   ORACLE   ###############################

def oracle(list_values:list, circuit_type:str):
    n=len(list_values[0]) # Number of elements in one string.
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    
    if (circuit_type == 'noancilla' or n==2):
        q1=QuantumRegister(n+1, "q")
        a1=QuantumCircuit(q1)
        a1.barrier()
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
            a1.barrier()
        
    elif circuit_type=='ancilla':
        r,pn,jn,kn=0,2,0,1
        q1=QuantumRegister(n*2, "q")
        a1=QuantumCircuit(q1)
        a1.barrier()
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
            a1.barrier()
    return a1
##############################  GROVER'S DIFFUSER  #############################
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
        r,pn,jn,kn=0,2,0,1
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
    ######### Apply Hadamard and X gates.
    a1.h(q1[n-1]) # Apply Hadamrd gate on the right of the target qubit n.
    a1.x(q1[[*range(n)]])
    a1.h(q1[[*range(n)]])
    #########
    return a1
#############################  ORACLE + DIFFUSER CIRCUIT  #############################
def grover(list_values:list, circuit_type:str):
    n=len(list_values[0])
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    assert len(set(list_values)) == len(list_values), 'You should not have a duplicate string value in your list.'
    if (circuit_type == 'noancilla' or n==2):
        q1=QuantumRegister(n+1, "q")
        a1=QuantumCircuit(q1)
        a1.append(oracle(list_values, circuit_type), [*range(n+1)]) # Add oracle.
        a1.append(diffuser(list_values, circuit_type), [*range(n)]) # Add diffuser.
    elif circuit_type =='ancilla':
        q1=QuantumRegister(n*2, "q")
        a1=QuantumCircuit(q1)
        a1.append(oracle(list_values, circuit_type), [*range(n*2)])
        a1.append(diffuser(list_values, circuit_type), [*range(n*2)])
    return a1

#####################  INITIALIZE THE CIRCUIT WITH BALANCED STATE  #####################
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

#####################              GROVER'S CIRCUIT               ##################### 
def grover_itera(list_values:list, circuit_type: str, number_iterations: int):
    n=len(list_values[0])
    assert n>=2, 'Length of input should be greater or equal to 2.'
    assert len(set(map(len, list_values))) == 1, 'The values on your list should have the same length.'
    assert len(set(list_values)) == len(list_values), 'You should not have a duplicate string value in your list.'
    
    circuit=initialize(list_values, circuit_type)

        ############### COMBINE: BALANCED STATE + ORACLE + DIFFUSER ###############
    # Iterate: (oracle+diffuser) + (oracle+diffuser) + ... .
    for i in range(number_iterations):
        circuit=circuit.combine(grover(list_values, circuit_type))
    
    circuit.measure([*range(n)],[*range(n)]) # Measure the n qubits.

    return circuit

