import unittest
from qiskit import *
from grover import *


class TestSearch(unittest.TestCase):

    def test_search(self):
        result = grover(['01011001'], 'noancilla')
        simulator=Aer.get_backend('qasm_simulator')
        count1=execute(result,simulator).result().get_counts()
        self.assertEqual(max(count1, key=int), '01011001')


        # 2nd test    
        result = grover(['111'], 'ancilla')
        simulator=Aer.get_backend('qasm_simulator')
        count1=execute(result,simulator).result().get_counts()
        self.assertEqual(max(count1, key=int), '111')


if __name__ == '__main__':
    unittest.main()