#!/usr/bin/env python3

from dataclasses import dataclass
import math
import numpy as np
from typing import List
import warnings

from .gates import Swap, Gate, CGate, CCGate
from .gates.utils import (
    create_double_controlled_matrix,
    create_controlled_matrix,
    create_matrix,
)

QUBIT_STARTING_STATE = np.zeros(2, dtype=np.complex128)
QUBIT_STARTING_STATE[0] = 1


@dataclass
class QubitGroup:
    """Helper class used in the simulator to keep track
    of which qubit sets have been entangled (for the sake
    of faster computation)."""

    qubits: List[int]
    state: np.ndarray

    def __hash__(self) -> int:
        qubit_string = ",".join([str(qubit) for qubit in self.qubits])
        return hash(qubit_string)


def probabilities_from_state(state: np.ndarray) -> np.ndarray:
    """Returns the probabilities corresponding to a quantum
    system state."""

    conjugate = state.conjugate()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # Ignore "np.complex128Warning: Casting np.complex128 values to real discards the imaginary part"
        # since that is precisely what we want.
        probabilities = np.multiply(state, conjugate).astype(float)

    return probabilities


def probability_dict_from_state(state: np.ndarray) -> np.ndarray:
    """Returns a dictionary of the probabilities corresponding
    to the specified state. States with a probability of 0 are
    omitted.
    """

    qubit_num = int(math.log2(len(state)))

    probabilities = probabilities_from_state(state)

    probability_dict = {}
    for i, probability in enumerate(probabilities):

        if probability == 0:
            continue

        state: str = ""

        remainder = i
        for j in reversed(range(qubit_num)):

            if remainder >= 2**j:
                state += "1"
                remainder -= 2**j
            else:
                state += "0"

        probability_dict[state] = probability

    return probability_dict


def is_in_ket0(qubit_group: QubitGroup) -> bool:
    """Indicate if a specified qubit group is in ket0 state.
    If the qubit group contains more than 1 qubit, a
    NotImplementedError is raised.
    """

    if len(qubit_group.qubits) != 1:
        raise NotImplementedError()

    return qubit_group.state.tolist()[0] == 1


def is_in_ket1(qubit_group: QubitGroup) -> bool:
    """Indicate if a specified qubit group is in ket1 state.
    If the qubit group contains more than 1 qubit, a
    NotImplementedError is raised.
    """

    if len(qubit_group.qubits) != 1:
        raise NotImplementedError()

    return qubit_group.state.tolist()[1] == 1


def initialize_qubit_groups(qubit_num: int) -> List[QubitGroup]:
    """Create a list of qubit groups where each qubit group contains
    exactly one qubit id.
    """
    qubit_groups: List[QubitGroup] = []
    for i in range(qubit_num):
        qubit_groups.append(QubitGroup(qubits=[i], state=QUBIT_STARTING_STATE))
    return qubit_groups


def get_sorted_state(qubit_group: QubitGroup) -> np.ndarray:
    """Return a sorted version of the state of a qubit group
    based on the order of the group's qubit ids.
    """
    qubit_num = len(qubit_group.qubits)

    sorting_order = [0] * (2**qubit_num)
    for i in range(2**qubit_num):

        remainder = i
        for j in reversed(range(qubit_num)):

            if remainder >= 2**j:
                sorting_order[i] += 2 ** (
                    qubit_num - qubit_group.qubits[qubit_num - j - 1] - 1
                )
                remainder -= 2**j

    sorted_state = [0] * 2**qubit_num
    for i in range(2**qubit_num):
        sorted_state[sorting_order[i]] = qubit_group.state[i]

    sorted_state = np.asarray(sorted_state, dtype=np.complex128)
    return sorted_state


def apply_gate(relevant_qubit_group: QubitGroup, gate: Gate) -> None:
    """Apply the action of the specified gate onto the selected
    qubit group in place.
    """
    target_qubit = relevant_qubit_group.qubits.index(gate.target_qubit)
    matrix = create_matrix(
        gate.matrix,
        target_qubit=target_qubit,
        qubit_num=len(relevant_qubit_group.qubits),
    )
    relevant_qubit_group.state = np.matmul(matrix, relevant_qubit_group.state)


def apply_cgate(relevant_qubit_group: QubitGroup, gate: CGate) -> None:
    """Apply the action of the specified controlled gate onto the
    selected qubit group in place.
    """
    target_qubit = relevant_qubit_group.qubits.index(gate.target_qubit)
    control_qubit = relevant_qubit_group.qubits.index(gate.control_qubit)
    matrix = create_controlled_matrix(
        gate.matrix,
        control_qubit=control_qubit,
        target_qubit=target_qubit,
        qubit_num=len(relevant_qubit_group.qubits),
    )
    relevant_qubit_group.state = np.matmul(matrix, relevant_qubit_group.state)


def apply_ccgate(relevant_qubit_group: QubitGroup, gate: CCGate) -> None:
    """Apply the action of the specified double controlled gate onto the
    selected qubit group in place.
    """
    target_qubit = relevant_qubit_group.qubits.index(gate.target_qubit)
    control_qubit1 = relevant_qubit_group.qubits.index(gate.control_qubit1)
    control_qubit2 = relevant_qubit_group.qubits.index(gate.control_qubit2)
    matrix = create_double_controlled_matrix(
        gate.matrix,
        control_qubit1=control_qubit1,
        control_qubit2=control_qubit2,
        target_qubit=target_qubit,
        qubit_num=len(relevant_qubit_group.qubits),
    )
    relevant_qubit_group.state = np.matmul(matrix, relevant_qubit_group.state)


def apply_swap_gate(qubit_groups: List[QubitGroup], gate: Swap) -> None:
    """Swap the indices of the qubits targetted by the swap gate
    in place.
    """
    for qubit_group in qubit_groups:
        for i in range(len(qubit_group.qubits)):
            if qubit_group.qubits[i] == gate.qubit1:
                qubit_group.qubits[i] = gate.qubit2

            elif qubit_group.qubits[i] == gate.qubit2:
                qubit_group.qubits[i] = gate.qubit1


def select_affected_qubit_group(
    qubit_groups: List[QubitGroup], qubit_id: int
) -> QubitGroup:
    """Select the qubit group whose qubit id
    is affected by the specified gate. Raise ValueError
    if no matching qubit group is found.
    """

    for qubit_group in qubit_groups:
        if qubit_id in qubit_group.qubits:
            return qubit_group

    raise ValueError(f"No matching qubit group found for qubit '{qubit_id}'")
