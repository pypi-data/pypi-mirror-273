'''
 Copyright 2023 Jack Morgan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from .quantum_linear_system import QuantumLinearSystemProblem
from qiskit.quantum_info import random_hermitian
import numpy as np
from scipy.stats import ortho_group

def RandomQLSP(number_qubits: int,
               maximum_condition_number: float,
               maximum_iterations_number: int = 100) :
    """
    The function RandomQLSP generates a random quantum linear system problem with a specified number of
    qubits. The function randomly draws Hermitian matrices until it finds a well conditioned system.
    
    :param number_qubits: The parameter "number_qubits" represents the number of qubits in the quantum
    linear system problem. It determines the size of the problem and the dimension of the matrix and
    vector involved.
    :type number_qubits: int
    :param maximum_condition_number: The maximum condition number is a threshold value that determines
    when to stop searching for a suitable problem. The condition number is a measure of how sensitive a
    problem is to changes in its input. In this case, it is the ratio of the largest eigenvalue to the
    smallest eigenvalue of the matrix A.
    :type maximum_condition_number: float
    :param maximum_iterations_number: The maximum number of random draws to search for a suitably
    conditioned matrix.
    :type maximum_condition_number: int
    :return: a QuantumLinearSystemProblem object, which is created using the A_matrix and b_vector
    variables.
    """
    condition_number = maximum_condition_number+1
    size = 2**number_qubits
    iterations = 0

    while condition_number > maximum_condition_number:
        
        # raise error if the number of iterations is exceeded.
        iterations+=1
        if iterations > maximum_iterations_number:
            raise Exception('Suitable random hermitian not found after maximum number of iterations')
        
        # randomly draw hermitian matrix.
        A_matrix = np.asmatrix(random_hermitian(size).data)
        b_vector = np.asarray(np.random.rand(size)).reshape((size,1))
        # check condition number
        A_eigen = np.linalg.eigvals(A_matrix)
        condition_number = abs(max(A_eigen,key=abs)/min(A_eigen,key=abs))

    # randomly generate normal b vector
    b_vector = np.asarray(np.random.rand(size)).reshape((size,1)) 
    b_vector = b_vector/np.linalg.norm(b_vector)
    
    return QuantumLinearSystemProblem(A_matrix, b_vector)

def ExampleQLSP(lam: float) -> QuantumLinearSystemProblem:
    """
    The function ExampleQLSP creates a QuantumLinearSystemProblem object with a given lambda value.
    
    :param lam: The parameter `lam` (short for lambda is a float value that is used to define the elements of the matrix
    `A_matrix`. The linear system is defined in equation 16 of [1]
    :type lam: float
    :return: a QuantumLinearSystemProblem object.
    References:
        [1]: Lee, Y., Joo, J., & Lee, S. (2019). 
        Hybrid quantum linear equation algorithm and its experimental test on ibm quantum experience. 
        Scientific reports, 9(1), 4778.
        `arxiv:1807.10651 <https://arxiv.org/abs/1807.10651>`_.
    """
    
    A_matrix = np.asmatrix([[0.5, lam-0.5],[lam-0.5,0.5]])
    b_vector = [1,0]
    return QuantumLinearSystemProblem(A_matrix, b_vector)

def ArbitraryExampleQLSP(eigenvalue_list: list[float], 
                         relevant_eigenvalue_list: list[float]) -> QuantumLinearSystemProblem:
    """
    The function `ArbitraryExampleQLSP` generates a Quantum Linear System Problem using given
    eigenvalues and relevant eigenvalues.
    
    :param eigenvalue_list: The `eigenvalue_list` parameter in the `ArbitraryExampleQLSP` function
    represents a list of eigenvalues that will be used to construct a Hermitian matrix.
    :type eigenvalue_list: list[float]
    :param relevant_eigenvalue_list: The `relevant_eigenvalue_list` parameter is a list of eigenvalues
    that are relevant for solving the quantum linear system problem. These eigenvalues will be used to
    compute the b_vector
    :type relevant_eigenvalue_list: list[float]
    :return: The function `ArbitraryExampleQLSP` returns a `QuantumLinearSystemProblem` object, which is
    created using the Hermitian matrix generated from the `eigenvalue_list` and a vector
    that is an equal superposition of the eigenvectors corresponding to the `relevant_eigenvalue_list` of that matrix.
    """
    def hermitian_matrix(eigenvalues):
        n = len(eigenvalues)
        ortho = ortho_group.rvs(dim=n)
        diag = np.diag(eigenvalues)
        matrix = np.matmul(ortho, diag)
        matrix = np.matmul(matrix, ortho.T)
        return matrix
    
    def equal_superposition_eigenvectors(eigenvalue_list, matrix):
        # Compute the eigenvectors of the matrix
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        
        # Initialize the superposition vector
        superposition_vector = np.zeros_like(eigenvectors[:,0], dtype=complex)
        
        # Iterate over each eigenvalue and add its eigenvector to the superposition vector
        for eigenvalue in eigenvalue_list:
            index = np.abs(eigenvalues - eigenvalue).argmin()
            superposition_vector += eigenvectors[:, index]
        
        # Normalize the superposition vector
        superposition_vector /= np.linalg.norm(superposition_vector)
        
        return superposition_vector
    
    A_matrix = hermitian_matrix(eigenvalue_list)
    b_vector = equal_superposition_eigenvectors(relevant_eigenvalue_list, A_matrix).astype(np.float64)

    return QuantumLinearSystemProblem(A_matrix, b_vector)



