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

import __future__

from .quantum_linear_system import QuantumLinearSystemSolver, QuantumLinearSystemProblem
from qiskit import transpile, QuantumCircuit
from qiskit.circuit.library import HamiltonianGate
from qiskit.circuit.library import PhaseEstimation, StatePreparation
from qiskit.quantum_info import Statevector
from qiskit_algorithms import AlgorithmError
from qiskit.providers import Backend
from qiskit_ibm_runtime import Sampler, Session
import numpy as np

def ideal_preprocessing(problem: QuantumLinearSystemProblem):
    """
    The `ideal_preprocessing` function computes the ideal eigenvalue list and eigenbasis projection of a
    QuantumLinearSystemProblem.
    
    :param problem: The `problem` parameter is an instance of the `QuantumLinearSystemProblem` class. It
    represents a linear system problem that needs to be solved using quantum computing techniques
    :return: The function `ideal_preprocessing` returns a tuple containing the eigenvalue list and
    eigenbasis projection list.
    """
    solution = QuantumLinearSystemSolver(problem=problem) # Classically solves the linear system problem

    eigenvalue_list = solution.eigenvalue_list
    eigenbasis_projection_list = solution.eigenbasis_projection_list

    return (eigenvalue_list, eigenbasis_projection_list)

def list_preprocessing(eigenvalue_list: list, 
                       eigenbasis_projection_list: list,
                       ):
    """
    The 'list_preprocessing' function returns a function that can be used instead of the 'estimate' method
    of the preprocessing algorithm classes. This can be used in lieu of repeating the preprocessing circuit
    when the output of the other preprocessing class is already known.
    
    :param eigenvalue_list: The `eigenvalue_list` is the eigenvalue_list output of another preprocessing function
    :param eigenbasis_projection_list: The `eigenbasis_projection_list` output of another preprocessing function
    :return: The `list_preprocessing` function is returning the `list_preprocessing_function` function,
    which takes a `QuantumLinearSystemProblem` as input and returns the `eigenvalue_list` and
    `eigenbasis_projection_list` provided as arguments to the outer function.
    """
    
    def list_preprocessing_function(problem:QuantumLinearSystemProblem):
        return eigenvalue_list, eigenbasis_projection_list
    return list_preprocessing_function

# The `QCL_QPE_IBM` class implements the Quantum Clock Quantum Phase Estimation (QCL-QPE) algorithm on
# IBM Quantum devices.
class Yalovetzky_preprocessing:
    """
        The function initializes the qcl-qpe preprocessing algorithm outlined in [1] with specified parameters.
        
        :param clock: The clock parameter represents the number of bits used to estimate the eigenvalues.
        It is used to calculate the default minimum probability (min_prob) in the
        __init__ method.
        :param backend: The `backend` parameter is used to specify the IBM Backend object that will evaulate
        the circuit.
        :param alpha: The alpha parameter is the initial overestimate of the largest eigenvalue of the system.
        This parameter is not needed if the max_eigenvalue is set.
        :param max_eigenvalue: The `max_eigenvalue` parameter is used to set the maximum eigenvalue for
        the quantum circuit. It determines the maximum value that can be measured for the eigenvalues of
        the observable being measured. If not specified, alpha will be used to determine the maximum eigenvalue 
        via algorithms 1 and 2 from [1].
        :param min_prob: The `min_prob` parameter is used to set the minimum probability value. If
        `min_prob` is not provided, it is set to `2**-clock`, where `clock` is another parameter

        References:
        [1]: Yalovetzky, R., Minssen, P., Herman, D., & Pistoia, M. (2021). 
            NISQ-HHL: Portfolio optimization for near-term quantum hardware. 
            `arXiv:2110.15958 <https://arxiv.org/abs/2110.15958>`_.
        """
    def __init__(self,
                 clock: int,
                 alpha: float = 50,
                 max_eigenvalue: float = None,
                 min_prob: float = None,
                 **kwargs,
                ):
        self.clock = clock
        if 'backend' in kwargs.keys():
            self.backend = kwargs['backend']
            self.get_result = self.get_result_backend

        elif 'session' in kwargs.keys():
            self.session = kwargs['session']
            self.get_result = self.get_result_session
            
        self.alpha = alpha
        self.max_eigenvalue = max_eigenvalue
        if min_prob == None:
           min_prob = 2**-clock
        self.min_prob = min_prob
    
    def get_result_backend(self):
        '''This method runs the QCL_QPE circuit with the specified backend and converts the results from two's complement.'''
        
        circ = self.construct_circuit(hamiltonian_gate=self.hamiltonian_simulation, state_preparation=self.state_preparation)
        backend = self.backend
        transp = transpile(circ, backend)
        result = backend.run(transp, shots=4000).result()
        counts = result.get_counts()
        tot = sum(counts.values())
        # translate results into integer representation of the bitstring and adjust for two's compliment
        result_dict = {(int(key,2) if key[0]=='0' else (int(key,2) - (2**(len(key))))) : value / tot for key, value in counts.items()}
        self.result = result_dict
        return result_dict

    def get_result_session(self):
        '''This method runs the QPE circuit with the ibm_runtime Sampler converts the results from two's complement. '''
        sampler = Sampler(self.session)
        backend = self.session.service.get_backend(self.session.backend())
        circ = self.construct_circuit(hamiltonian_gate=self.hamiltonian_simulation, state_preparation=self.state_preparation)
        transp = transpile(circ, backend)
        print('circuit depth = ', transp.depth())
        max_key = 2**circ.num_clbits
        result = sampler.run(transp).result()
        
        result_dict = {(key if 2*key<max_key else (key - max_key)) : value for key, value in result.quasi_dists[0].items()}

        return result_dict
    
    def test_scale(self, scale: float):
        '''This method performs algorithm two from [1].'''
        Gamma = scale/(2**self.clock) # attempt to over approximate the eigenvalue
        self.hamiltonian_simulation = HamiltonianGate(self.problem.A_matrix, -2*np.pi*Gamma)
        results = self.get_result() # get the result
        abs_eigens = {abs(eig) : prob for eig, prob in results.items() if prob > self.min_prob}
        
        if 0 in abs_eigens.keys():
            test = abs_eigens[0] # determine the probability of measureing 0
        else:
            test = 0
        # return a boolean if the eigenvalue is overapproximated
        if test>(1-self.min_prob):
            return True
        else:
            return False
    
    def find_scale(self, alpha: float):
        '''This method combines algorithm 1 and 2 [1]. Combined these algorithms determine the optimal time 
        step parameter of the hamiltonian simulation, if a maximum eigenvalue or hamiltonian gate are not provided.'''
        scale = 1/alpha # initial scale
        self.hamiltonian_simulation = HamiltonianGate(self.problem.A_matrix, -2*np.pi*scale) # set gate
        over_approximation = self.test_scale(scale) # verify over approximation
        while over_approximation == False:
            scale /= 2**(self.clock-1)
            over_approximation = self.test_scale(scale)
        
        x = 0 
        target = int((2**(self.clock-1)-1))
        
        # iteratively adjust scale until the largest eigenvalue is equal to the largest bitstring without overflow
        while x != target:
            self.hamiltonian_simulation = HamiltonianGate(self.problem.A_matrix, -2*np.pi*scale)
            results = self.get_result()
            eigens = {eig : prob for eig, prob in results.items() if prob > self.min_prob}  
            x = abs(max(eigens.keys(), key=abs))
            
            if not x == 0:
                scale /= x    
            
            scale *= target
            
        return scale
    
    def adjust_clock(self):
        '''This method determined the minimum number of bits needed to distinguish the lowest eigenvalue of interest from 0,
        which is the required number of bits for eigenvalue inversion'''
        min_eig = None
        # while the minimum eigenvalue is indistinguishable from zero, increase the clock by 1 bit.
        while min_eig == None:
            results = self.get_result(self.scale)
            eigens = {eig : prob for eig, prob in results.items() if prob > self.min_prob}
            test = 0
            # if zero is a relevant eigenvalue, increase the clock.
            if 0 in eigens.keys():
                test = eigens[0]
            if test > self.min_prob: 
                self.clock += 1
                self.min_prob /= 2 
            # if the clock is at the set end point, break the loop.
            elif self.clock >= self.max_clock:
                min_eig = 0
            # if the minimum eigenvalue is not zero, set the eigenvalue.
            else:
                min_eig = min(eigens.keys(), key=abs)
    
        return self.clock
    
    def construct_circuit(self, hamiltonian_gate: QuantumCircuit, state_preparation: QuantumCircuit):
        '''Constructs QCL_QPE circuit for a given hamiltonian gate'''
        
        circ = QuantumCircuit(hamiltonian_gate.num_qubits+1, self.clock)
        circ.append(state_preparation, list(range(1, circ.num_qubits)))
        for clbit in range(self.clock):
            if clbit!=0:
                circ.initialize([1,0],[0])
            circ.h(0)
            power=2**(self.clock-clbit-1)
            ham = hamiltonian_gate.power(power).control()
            circ.append(ham, circ.qubits)
            
            for i in reversed(range(clbit)):
                
                if i < self.clock:   
                    N = (2**(i+2))
                    
                    control = clbit-i-1
                    with circ.if_test((control,1)) as passed:
                        circ.p(-np.pi*2/N,0)
            circ.h(0)
            circ.measure(0,[clbit])
        return circ
    
    def estimate(self, problem: QuantumLinearSystemProblem):
        '''Returns a clock-bit estimation of the relevant eigenvalues, and the projection of 
        |b> in the eigenbasis of A.'''
        self.problem=problem

         # If the state_preparation is not specified in the problem, use the standard StatePreparation
        
        if getattr(problem, 'state_preparation', None) is None:
            
            self.state_preparation = StatePreparation(Statevector(problem.b_vector))
        
        else:
            self.state_preparation = problem.state_preparation
        
        # If the hamiltonian simulation is not specified in the problem, use the standard HamiltonianGate
        if getattr(problem, 'hamiltonian_simulation', None) is None:
            if self.max_eigenvalue == None:
                self.scale = self.find_scale(self.alpha)
            else:
                self.scale = abs((0.5-2**-self.clock)/self.max_eigenvalue)
                self.hamiltonian_simulation = HamiltonianGate(problem.A_matrix, -2*np.pi*self.scale)
        
        else:
            self.hamiltonian_simulation = problem.hamiltonian_simulation

        
        if hasattr(self, "max_clock"):
            self.adjust_clock()
            self.scale = abs((0.5-2**-self.clock)/self.max_eigen)
            
        if not hasattr(self, "result"):
            self.get_result(self.scale)
  
        eigenvalue_list = [eig/(self.scale*2**(self.clock)) for eig in self.result.keys() if self.result[eig] > self.min_prob]
        eigenbasis_projection_list = [self.result[eig] for eig in self.result.keys() if self.result[eig] > self.min_prob]
        return eigenvalue_list, eigenbasis_projection_list
    
# The `Lee_preprocessing` class is used for preprocessing in Quantum Phase Estimation algorithms,
# including circuit construction and eigenvalue estimation.
class Lee_preprocessing:
    def __init__(self,
                 num_eval_qubits: int,
                 max_eigenvalue: float,
                 wait_for_result: bool = True,
                 **kwargs
                 ):
        """
        The above code defines a class with methods for estimating eigenvalues and eigenbasis projection of a
        given problem using cannonical quantum phase estimation.
        
        :param backend: The `backend` parameter is the quantum backend on which the circuit will be
        executed. It represents the physical device or simulator that will run the quantum circuit
        :param num_eval_qubits: The parameter `num_eval_qubits` represents the number of qubits used in
        the phase estimation algorithm. It determines the precision of the estimated eigenvalues
        :param max_eigenvalue: The `max_eigenvalue` parameter represents an upper bound on the
        eigenvalues of the Hamiltonian matrix. It is used in the `estimate` method to scale the
        Hamiltonian simulation. If the `max_eigenvalue` is not provided and the problem does
        not specify a Hamiltonian simulation gate, an `AlgorithmError` is raised
        """
        self.num_eval_qubits = num_eval_qubits
        self.max_eigenvalue = max_eigenvalue
        self.wait_for_result = wait_for_result
        self.get_result = self.get_result_function(kwargs)

    def construct_circuit(self, 
                          hamiltonian_simulation: QuantumCircuit,
                          state_preparation: QuantumCircuit,
                          ):
        """
        The function constructs a quantum circuit by appending a state preparation circuit, a phase
        estimation circuit, and measurement operations.
        
        :param hamiltonian_simulation: The `hamiltonian_simulation` parameter is an object that
        represents the Hamiltonian simulation. It likely contains information about the Hamiltonian that
        you want to simulate, such as the number of qubits it acts on and the specific gates or
        operations that need to be applied
        :param state_preparation: The `state_preparation` parameter is a quantum circuit that prepares
        the initial state of the quantum system. It is applied to the qubits starting from index
        `self.num_eval_qubits` up to the total number of qubits in the circuit
        :return: a QuantumCircuit object.
        """
        circuit = QuantumCircuit(self.num_eval_qubits+hamiltonian_simulation.num_qubits, self.num_eval_qubits)
        circuit.append(state_preparation, range(self.num_eval_qubits, circuit.num_qubits))
        circuit.append(PhaseEstimation(self.num_eval_qubits, hamiltonian_simulation), circuit.qubits)
        circuit.measure(list(range(self.num_eval_qubits))[::-1], range(self.num_eval_qubits))
        return circuit
    
    def get_result_function(self, kwargs):
        """
        The function `get_result_function` takes a backend as input and returns a function that
        preprocesses a circuit, transpiles it using the backend, runs it on an ionq simulator, and
        returns the result.
        
        :param backend: The `backend` parameter is the target backend where the circuit will be executed.
        It could be a specific quantum device or a simulator
        :return: The function `get_result_preprocessing` is being returned.
        """
        if 'backend' in kwargs.keys():
            backend = kwargs['backend']
            if 'shots' in kwargs.keys():
                shots=kwargs['shots']
            else:
                shots=4000
            def get_result_preprocessing(circ):
                transp = transpile(circ, backend)
                self.depth = transp.depth()
                if 'noise_model' in kwargs.keys():
                    job = backend.run(transp, noise_model=kwargs['noise_model'], shots=shots)
                else:
                    job = backend.run(transp, shots=shots)
                if self.wait_for_result:
                    result=job.result()
                    counts = result.get_counts()
                    tot = sum(counts.values())
                    result_dict = {(int(key,2) if key[0]=='0' else (int(key,2) - (2**(len(key))))) : value / tot for key, value in counts.items()}
                    return result_dict
                else:
                    return job
            return get_result_preprocessing
        if 'session' in kwargs.keys():
            session = kwargs['session']
            sampler = Sampler(session)
            backend = session.service.get_backend(session.backend())
            def get_session_result_preprocessing(circ):
                max_key = 2**circ.num_clbits 
                transp = transpile(circ, backend)
                self.depth = transp.depth()
                job = sampler.run(transp)
                if self.wait_for_result:
                    result = job.result()
                    result_dict = {(key if 2*key<max_key else (key - max_key)) : value for key, value in result.quasi_dists[0].items()}
                    return result_dict
                else:
                    return job
            return get_session_result_preprocessing

    
    def estimate(self, problem):
        """
        The `estimate` function estimates the eigenvalues and eigenbasis projections of a given problem
        using a Hamiltonian simulation and state preparation.
        
        :param problem: The `problem` parameter is the quantum linear system problem for which the eigenvalues
            and eigenbasis projection will be calculated.
        :return: The function `estimate` returns two lists: `eigenvalue_list` and
        `eigenbasis_projection_list`.
        """
        # If hamiltonian_simulation is not specified in the problem, use the HamiltonianGate from qiskit
        # with the scale calculated by the max_eigenvalue parameter. If neither are specified,
        # return an algorithm error
        if getattr(problem, 'hamiltonian_simulation', None) is None:
            if self.max_eigenvalue == None:
                raise AlgorithmError('An upper bound on the eigenvalues is needed')
            
            scale = abs((0.5-2**-self.num_eval_qubits)/self.max_eigenvalue)
            hamiltonian_simulation = HamiltonianGate(problem.A_matrix, -2*np.pi*scale)
        
        else:
            hamiltonian_simulation = problem.hamiltonian_simulation
            scale=1
        

        # If the state_preparation is not specified in the problem, use the standard StatePreparation
        
        if getattr(problem, 'state_preparation', None) is None:
            
            state_preparation = StatePreparation(Statevector(problem.b_vector))
        
        else:
            state_preparation = problem.state_preparation

        # Construct circuit

        circ = self.construct_circuit(hamiltonian_simulation, state_preparation)
        result_dict = self.get_result(circ)
        if self.wait_for_result:
            min_prob = 2**-self.num_eval_qubits
            eigenvalue_list = [eig/(scale*2**(self.num_eval_qubits)) for eig in result_dict.keys() if result_dict[eig] > min_prob]
            eigenbasis_projection_list = [result_dict[eig] for eig in result_dict.keys() if result_dict[eig] > min_prob]
            return eigenvalue_list, eigenbasis_projection_list
        else:
            return result_dict

class Iterative_QPE_Preprocessing:
    """
        The function follows the iterative procedure to scale the QLSP outlined in [1] with specified parameters.
        The actual phase estimation circuit is a standard QPE circuit as opposed to QCL_QPE in Yalovetsky_preprocessing.
        
        :param clock: The clock parameter represents the number of bits used to estimate the eigenvalues.
        It is used to calculate the default minimum probability (min_prob) in the
        __init__ method.
        :param backend: The `backend` parameter is used to specify the IBM Backend object that will evaulate
        the circuit.
        :param alpha: The alpha parameter is the initial overestimate of the largest eigenvalue of the system.
        This parameter is not needed if the max_eigenvalue is set.
        :param max_eigenvalue: The `max_eigenvalue` parameter is used to set the maximum eigenvalue for
        the quantum circuit. It determines the maximum value that can be measured for the eigenvalues of
        the observable being measured. If not specified, alpha will be used to determine the maximum eigenvalue 
        via algorithms 1 and 2 from [1].
        :param min_prob: The `min_prob` parameter is used to set the minimum probability value. If
        `min_prob` is not provided, it is set to `2**-clock`, where `clock` is another parameter

        References:
        [1]: Yalovetzky, R., Minssen, P., Herman, D., & Pistoia, M. (2021). 
            NISQ-HHL: Portfolio optimization for near-term quantum hardware. 
            `arXiv:2110.15958 <https://arxiv.org/abs/2110.15958>`_.
        """
    def __init__(self,
                 clock: int,
                 alpha: float = 50,
                 max_eigenvalue: float = None,
                 min_prob: float = None,
                 **kwargs):
        self.clock = clock
        if 'backend' in kwargs.keys():
            self.backend = kwargs['backend']
            self.get_result = self.get_result_backend

        elif 'session' in kwargs.keys():
            self.session = kwargs['session']
            self.get_result = self.get_result_session
            
        self.alpha = alpha
        self.max_eigenvalue = max_eigenvalue
        if min_prob == None:
           min_prob = 2**-clock
        self.min_prob = min_prob


    def get_result_backend(self):
        '''This method runs the QPE circuit on the specified backendand converts the results from two's complement. '''
        
        circ = self.construct_circuit(hamiltonian_simulation=self.hamiltonian_simulation, state_preparation=self.state_preparation)
        backend = self.backend
        transp = transpile(circ, backend)
        result = backend.run(transp, shots=4000).result()
        counts = result.get_counts()
        tot = sum(counts.values())
        # translate results into integer representation of the bitstring and adjust for two's compliment
        result_dict = {(int(key,2) if key[0]=='0' else (int(key,2) - (2**(len(key))))) : value / tot for key, value in counts.items()}
        self.result = result_dict
        return result_dict

    def get_result_session(self):
        '''This method runs the QPE circuit with the ibm_runtime Sampler converts the results from two's complement. '''
        sampler = Sampler(self.session)
        backend = self.session.service.get_backend(self.session.backend())
        circ = self.construct_circuit(hamiltonian_simulation=self.hamiltonian_simulation, state_preparation=self.state_preparation)
        transp = transpile(circ, backend)
        self.depth = transp.depth()
        max_key = 2**circ.num_clbits
        result = sampler.run(transp).result()
        
        result_dict = {(key if 2*key<max_key else (key - max_key)) : value for key, value in result.quasi_dists[0].items()}
        self.result = result_dict
        return result_dict
    
    def test_scale(self, scale: float):
        '''This method performs algorithm two from [1].'''
        Gamma = scale/(2**self.clock) # attempt to over approximate the eigenvalue
        self.hamiltonian_simulation = HamiltonianGate(self.problem.A_matrix, -2*np.pi*Gamma)
        results = self.get_result() # get the result
        abs_eigens = {abs(eig) : prob for eig, prob in results.items() if prob > self.min_prob}
        test = abs_eigens[0] # determine the probability of measureing 0

        # return a boolean if the eigenvalue is overapproximated
        if test>(1-self.min_prob):
            return True
        else:
            return False
    
    def find_scale(self, alpha: float):
        '''This method combines algorithm 1 and 2 [1]. Combined these algorithms determine the optimal time step parameter of the hamiltonian simulation, if a maximum eigenvalue or hamiltonian gate are not provided.'''
        scale = 1/alpha # initial scale
        self.hamiltonian_simulation = HamiltonianGate(self.problem.A_matrix, -2*np.pi*scale) # set gate
        over_approximation = self.test_scale(scale) # verify over approximation
        while over_approximation == False:
            scale /= 2**(self.clock-1)
            over_approximation = self.test_scale(scale)
        
        x = 0 
        target = int((2**(self.clock-1)-1))
        
        # iteratively adjust scale until the largest eigenvalue is equal to the largest bitstring without overflow
        while x != target:
            self.hamiltonian_simulation = HamiltonianGate(self.problem.A_matrix, -2*np.pi*scale)
            results = self.get_result()
            eigens = {eig : prob for eig, prob in results.items() if prob > self.min_prob}  
            x = abs(max(eigens.keys(), key=abs))
            
            if not x == 0:
                scale /= x    
            
            scale *= target
            
        return scale
    
    def adjust_clock(self):
        '''This method determined the minimum number of bits needed to distinguish the lowest eigenvalue of interest from 0,
        which is the required number of bits for eigenvalue inversion'''
        min_eig = None
        # while the minimum eigenvalue is indistinguishable from zero, increase the clock by 1 bit.
        while min_eig == None:
            results = self.get_result(self.scale)
            eigens = {eig : prob for eig, prob in results.items() if prob > self.min_prob}
            test = 0
            # if zero is a relevant eigenvalue, increase the clock.
            if 0 in eigens.keys():
                test = eigens[0]
            if test > self.min_prob: 
                self.clock += 1
                self.min_prob /= 2 
            # if the clock is at the set end point, break the loop.
            elif self.clock >= self.max_clock:
                min_eig = 0
            # if the minimum eigenvalue is not zero, set the eigenvalue.
            else:
                min_eig = min(eigens.keys(), key=abs)
    
        return self.clock
    
    def construct_circuit(self, 
                          hamiltonian_simulation: QuantumCircuit,
                          state_preparation: QuantumCircuit,
                          ):
        """
        The function constructs a quantum circuit by appending a state preparation circuit, a phase
        estimation circuit, and measurement operations.
        
        :param hamiltonian_simulation: The `hamiltonian_simulation` parameter is an object that
        represents the Hamiltonian simulation. It likely contains information about the Hamiltonian that
        you want to simulate, such as the number of qubits it acts on and the specific gates or
        operations that need to be applied
        :param state_preparation: The `state_preparation` parameter is a quantum circuit that prepares
        the initial state of the quantum system. It is applied to the qubits starting from index
        `self.num_eval_qubits` up to the total number of qubits in the circuit
        :return: a QuantumCircuit object.
        """
        circuit = QuantumCircuit(self.clock+hamiltonian_simulation.num_qubits, self.clock)
        circuit.append(state_preparation, range(self.clock, circuit.num_qubits))
        circuit.append(PhaseEstimation(self.clock, hamiltonian_simulation), circuit.qubits)
        circuit.measure(list(range(self.clock))[::-1], range(self.clock))
        return circuit
    
    def estimate(self, problem: QuantumLinearSystemProblem):
        '''Returns a clock-bit estimation of the relevant eigenvalues, and the projection of 
        |b> in the eigenbasis of A.'''
        self.problem=problem

         # If the state_preparation is not specified in the problem, use the standard StatePreparation
        
        if getattr(problem, 'state_preparation', None) is None:
            
            self.state_preparation = StatePreparation(Statevector(problem.b_vector))
        
        else:
            self.state_preparation = problem.state_preparation
        
        # If the hamiltonian simulation is not specified in the problem, use the standard HamiltonianGate
        if getattr(problem, 'hamiltonian_simulation', None) is None:
            if self.max_eigenvalue == None:
                self.scale = self.find_scale(self.alpha)
            else:
                self.scale = abs((0.5-2**-self.clock)/self.max_eigenvalue)
                self.hamiltonian_simulation = HamiltonianGate(problem.A_matrix, -2*np.pi*self.scale)
        
        else:
            self.hamiltonian_simulation = problem.hamiltonian_simulation

        
        if hasattr(self, "max_clock"):
            self.adjust_clock()
            self.scale = abs((0.5-2**-self.clock)/self.max_eigen)
            
        if not hasattr(self, "result"):
            self.get_result()
  
        eigenvalue_list = [eig/(self.scale*2**(self.clock)) for eig in self.result.keys() if self.result[eig] > self.min_prob]
        eigenbasis_projection_list = [self.result[eig] for eig in self.result.keys() if self.result[eig] > self.min_prob]
        return eigenvalue_list, eigenbasis_projection_list