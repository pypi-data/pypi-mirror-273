#!/usr/bin/env python3

import numpy as np
from typing import List, Dict

from .circuit import Circuit
from .gates import IGate, Swap, Gate, CGate, CCGate
from .utils import (
    QubitGroup,
    is_in_ket0,
    is_in_ket1,
    initialize_qubit_groups,
    get_sorted_state,
    apply_gate,
    apply_cgate,
    apply_ccgate,
    apply_swap_gate,
    select_affected_qubit_group,
)


def merge_qubit_groups(
    relevant_groups: List[QubitGroup], total_groups: List[QubitGroup]
) -> QubitGroup:
    """Merge selected (relevant) qubit groups into a single qubit group
    and remove the previous qubit groups from the list of all qubit groups.
    The removal happens in place, while the merged qubit group is returned.
    """

    # remove duplicates
    relevant_groups = list(set(relevant_groups))

    merged_qubit_group = relevant_groups[0]
    for qubit_group in relevant_groups[1:]:
        merged_qubit_group.qubits.extend(qubit_group.qubits)
        merged_qubit_group.state = np.kron(merged_qubit_group.state, qubit_group.state)

        total_groups.remove(qubit_group)

    return merged_qubit_group


def aggregate_qubit_groups(qubit_groups: List[QubitGroup]) -> QubitGroup:
    """Combine a list of qubit groups into a new joined qubit group."""
    aggregated_qubit_group = qubit_groups[0]
    for qubit_group in qubit_groups[1:]:
        aggregated_qubit_group.qubits.extend(qubit_group.qubits)
        aggregated_qubit_group.state = np.kron(
            aggregated_qubit_group.state, qubit_group.state
        )
    return aggregated_qubit_group


class QuaSim:
    """Quantum circuit simulator used to evaluate quantum
    circuits.
    """

    def __init__(self) -> None:
        pass

    def evaluate(self, circuits: List[Circuit]) -> None:
        """Evaluates a list of quantum circuits and stores the
        state at the end of each circuit in circuit.state."""

        for circuit in circuits:
            self.evaluate_circuit(circuit)

    def evaluate_circuit(self, circuit: Circuit) -> None:
        """Evaluates a quantum circuit and stores the
        state at the end of the circuit in circuit.state."""

        if circuit.state is not None:
            return circuit.state

        qubit_groups = initialize_qubit_groups(circuit.qubit_num)

        for gate in circuit.gates:
            if type(gate) == Swap:
                self._apply_swap_gate(qubit_groups, gate)
                continue

            if issubclass(gate.__class__, Gate):
                self._apply_gate(qubit_groups, gate)

            elif issubclass(gate.__class__, CGate):
                self._apply_cgate(qubit_groups, gate)

            elif issubclass(gate.__class__, CCGate):
                self._apply_ccgate(qubit_groups, gate)

            else:
                raise NotImplementedError(
                    f"Unknown gate type for {gate} ({type(gate)})"
                )

        aggregated_qubit_group = aggregate_qubit_groups(qubit_groups)

        sorted_state = get_sorted_state(aggregated_qubit_group)

        circuit.set_state(sorted_state)

    def _apply_swap_gate(self, qubit_groups: List[QubitGroup], gate: Swap) -> None:
        apply_swap_gate(qubit_groups, gate)

    def _apply_gate(self, qubit_groups: List[QubitGroup], gate: Gate) -> None:
        target_qubit_group = select_affected_qubit_group(
            qubit_groups, qubit_id=gate.target_qubit
        )

        apply_gate(target_qubit_group, gate)

    def _apply_cgate(self, qubit_groups: List[QubitGroup], gate: CGate) -> None:
        control_qubit_group = select_affected_qubit_group(
            qubit_groups, qubit_id=gate.control_qubit
        )
        target_qubit_group = select_affected_qubit_group(
            qubit_groups, qubit_id=gate.target_qubit
        )

        if len(control_qubit_group.qubits) == 1:
            # Conrol qubit is inactive
            if is_in_ket0(control_qubit_group):
                pass
            # Control qubit is active
            elif is_in_ket1(control_qubit_group):
                apply_gate(target_qubit_group, gate)
            # Control qubit is in superposition state
            else:
                merged_qubit_group = merge_qubit_groups(
                    relevant_groups=[control_qubit_group, target_qubit_group],
                    total_groups=qubit_groups,
                )
                apply_cgate(merged_qubit_group, gate)

        else:
            merged_qubit_group = merge_qubit_groups(
                relevant_groups=[control_qubit_group, target_qubit_group],
                total_groups=qubit_groups,
            )
            apply_cgate(merged_qubit_group, gate)

    def _apply_ccgate(self, qubit_groups: List[QubitGroup], gate: CCGate) -> None:
        control_qubit1_group = select_affected_qubit_group(
            qubit_groups, qubit_id=gate.control_qubit1
        )
        control_qubit2_group = select_affected_qubit_group(
            qubit_groups, qubit_id=gate.control_qubit2
        )
        target_qubit_group = select_affected_qubit_group(
            qubit_groups, qubit_id=gate.target_qubit
        )

        if (
            len(control_qubit1_group.qubits) == 1
            and len(control_qubit2_group.qubits) == 1
        ):

            # Control qubit 1 is inactive
            if is_in_ket0(control_qubit1_group):
                pass

            # Control qubit 1 is active
            elif is_in_ket1(control_qubit1_group):

                # Control qubit 2 is inactive
                if is_in_ket0(control_qubit2_group):
                    pass

                # Control qubit 2 is active
                elif is_in_ket1(control_qubit2_group):
                    apply_gate(target_qubit_group, gate)

                # Control qubit 2 is in superposition
                else:
                    equivalent_cgate = CGate(
                        control_qubit=gate.control_qubit2,
                        target_qubit=gate.target_qubit,
                    )
                    equivalent_cgate.matrix = gate.matrix

                    merged_qubit_group = merge_qubit_groups(
                        relevant_groups=[
                            control_qubit2_group,
                            target_qubit_group,
                        ],
                        total_groups=qubit_groups,
                    )
                    apply_cgate(merged_qubit_group, equivalent_cgate)

            # Control qubit 1 is in superposition
            else:

                # Control qubit 2 is inactive
                if is_in_ket0(control_qubit2_group):
                    pass

                # Control qubit 2 is active
                elif is_in_ket1(control_qubit2_group):
                    equivalent_cgate = CGate(
                        control_qubit=gate.control_qubit1,
                        target_qubit=gate.target_qubit,
                    )
                    equivalent_cgate.matrix = gate.matrix

                    merged_qubit_group = merge_qubit_groups(
                        relevant_groups=[
                            control_qubit1_group,
                            target_qubit_group,
                        ],
                        total_groups=qubit_groups,
                    )
                    apply_cgate(merged_qubit_group, equivalent_cgate)

                # Control qubit 2 is in superposition
                else:
                    merged_qubit_group = merge_qubit_groups(
                        relevant_groups=[
                            control_qubit1_group,
                            control_qubit2_group,
                            target_qubit_group,
                        ],
                        total_groups=qubit_groups,
                    )
                    apply_ccgate(merged_qubit_group, gate)

        elif (
            len(control_qubit1_group.qubits) == 1
        ):  # and control qubit 2 group contains multiple qubits

            # Control qubit 1 is inactive
            if is_in_ket0(control_qubit1_group):
                pass

            # Control qubit 1 is active
            elif is_in_ket1(control_qubit1_group):
                equivalent_cgate = CGate(
                    control_qubit=gate.control_qubit2,
                    target_qubit=gate.target_qubit,
                )
                equivalent_cgate.matrix = gate.matrix

                merged_qubit_group = merge_qubit_groups(
                    relevant_groups=[
                        control_qubit2_group,
                        target_qubit_group,
                    ],
                    total_groups=qubit_groups,
                )
                apply_cgate(merged_qubit_group, equivalent_cgate)

            # Control qubit 1 is in superposition
            else:
                merged_qubit_group = merge_qubit_groups(
                    relevant_groups=[
                        control_qubit1_group,
                        control_qubit2_group,
                        target_qubit_group,
                    ],
                    total_groups=qubit_groups,
                )
                apply_ccgate(merged_qubit_group, gate)

        elif (
            len(control_qubit2_group.qubits) == 1
        ):  # and control qubit 1 group contains multiple qubits

            # Control qubit 2 is inactive
            if is_in_ket0(control_qubit2_group):
                pass

            # Control qubit 2 is active
            elif is_in_ket1(control_qubit2_group):
                equivalent_cgate = CGate(
                    control_qubit=gate.control_qubit1,
                    target_qubit=gate.target_qubit,
                )
                equivalent_cgate.matrix = gate.matrix

                merged_qubit_group = merge_qubit_groups(
                    relevant_groups=[
                        control_qubit1_group,
                        target_qubit_group,
                    ],
                    total_groups=qubit_groups,
                )
                apply_cgate(merged_qubit_group, equivalent_cgate)

            # Control qubit 2 is in superposition
            else:
                merged_qubit_group = merge_qubit_groups(
                    relevant_groups=[
                        control_qubit1_group,
                        control_qubit2_group,
                        target_qubit_group,
                    ],
                    total_groups=qubit_groups,
                )
                apply_ccgate(merged_qubit_group, gate)

        # both qubit groups contain more than 1 qubit
        else:
            merged_qubit_group = merge_qubit_groups(
                relevant_groups=[
                    control_qubit1_group,
                    control_qubit2_group,
                    target_qubit_group,
                ],
                total_groups=qubit_groups,
            )
            apply_ccgate(merged_qubit_group, gate)
