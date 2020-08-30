# Grover's Algorithm

This project is the result of the 3-months [QOSF](https://qosf.org/) mentorship progam. 

The project is the exploration of the designs of Grover's algorithm (ancilla and non-ancilla qubits). Also, we have done complexity analysis of each design on different qubit-number designs to see how the complexity changes by increasing the number of qubits of the length code of the element to be searched for.


## Getting Started
open the terminal
```
git clone https://github.com/moustafa-7/Grover-s-Algorithm-QOSF.git
``` 
```
cd Grover-s-Algorithm-QOSF
```
installing all dependencies
```
pip install -r requirements.txt
```


### How to use

check the file [src/Grover/main.ipynb](https://github.com/moustafa-7/Grover-s-Algorithm-QOSF/blob/master/src/Grover/main.ipynb) to see examples and how to use


## Running the tests
navigate to **src/Grover** and then run this command
```
python3 grover.py
```

## Some plots
* Success probability of the ancilla design (length of string = 3)
![image](src/Different%20Designs%20Comparison/ancilla_success_prob.png)

* Success probability of the noancilla design (length of string = 3)
![image](src/Different%20Designs%20Comparison/noancilla_success_prob.png)

* length of input string VS Number of computations (u3 + cx gates) used
![image](src/Different%20Designs%20Comparison/computations.png)




## Authors

The project was done by:
*  **Omar Ali** s-omar.hussein@zewailcity.edu.eg
*  [**Walid El Maouaki**](https://github.com/walid-mk)
*  [**Moustafa Elsayed**](https://github.com/moustafa-7) 

under the supervision of [**Dr. Yuval Sanders**](https://researchers.mq.edu.au/en/persons/yuval-sanders/publications/).

## License
Apache License 2.0<br/>
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/moustafa-7/Grover-s-Algorithm-QOSF/blob/master/LICENSE) file for details
