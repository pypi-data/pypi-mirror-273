import numpy as np
from scipy.linalg import dft

def quantum_phase_estimation(unitary_operator, num_qubits):
    """
    Perform Quantum Phase Estimation (QPE) algorithm to estimate phase from a unitary operator.

    Parameters:
    - unitary_operator: Unitary operator for phase estimation.
    - num_qubits: Number of qubits for the quantum state.

    Returns:
    - estimated_state: Estimated quantum state after phase estimation.
    """
    quantum_state = np.ones(2**num_qubits) / np.sqrt(2**num_qubits)
    qft_matrix = dft(2**num_qubits, scale='sqrtn')
    quantum_state = qft_matrix @ quantum_state

    for _ in range(num_qubits):
        quantum_state = unitary_operator @ quantum_state

    inverse_qft_matrix = np.conj(qft_matrix).T
    estimated_state = inverse_qft_matrix @ quantum_state

    return estimated_state