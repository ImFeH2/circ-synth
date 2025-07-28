from typing import List, Tuple, Optional
from itertools import combinations_with_replacement
import time

from core import Gate, Circuit

class ExactCircuitSynthesis:
    def __init__(self, available_gates: List[Gate], max_gates: int = 15, enable_pruning: bool = True):
        self.available_gates = available_gates
        self.max_gates = max_gates
        self.enable_pruning = enable_pruning
        self._search_stats = {'nodes_explored': 0, 'nodes_pruned': 0}

    def synthesize(self,
                   target_truth_table: List[Tuple[Tuple[int, ...], Tuple[int, ...]]],
                   input_names: List[str],
                   output_names: List[str]) -> Optional[Circuit]:
        self._reset_stats()

        print(f"Starting synthesis: {len(input_names)} inputs -> {len(output_names)} outputs")

        total_start_time = time.time()

        for gate_limit in range(1, self.max_gates + 1):
            start_time = time.time()
            print(f"Trying {gate_limit} gates...", end=' ')

            result = self._search_with_gate_limit(
                target_truth_table, input_names, output_names, gate_limit
            )

            elapsed_time = time.time() - start_time

            if result:
                total_elapsed = time.time() - total_start_time
                print(f"Found solution! (time: {elapsed_time:.3f}s)")
                print(f"Total time: {total_elapsed:.3f}s")
                print(f"Search stats: explored {self._search_stats['nodes_explored']} nodes, "
                      f"pruned {self._search_stats['nodes_pruned']} nodes")
                return result
            else:
                print(f"No solution (time: {elapsed_time:.3f}s)")

        total_elapsed = time.time() - total_start_time
        print(f"No solution found within {self.max_gates} gates limit")
        print(f"Total time: {total_elapsed:.3f}s")
        return None

    def _search_with_gate_limit(self,
                                target_truth_table: List[Tuple[Tuple[int, ...], Tuple[int, ...]]],
                                input_names: List[str],
                                output_names: List[str],
                                gate_limit: int) -> Optional[Circuit]:
        initial_circuit = Circuit(input_names, output_names)
        return self._backtrack_search(initial_circuit, target_truth_table, gate_limit)

    def _backtrack_search(self,
                          circuit: Circuit,
                          target_truth_table: List[Tuple[Tuple[int, ...], Tuple[int, ...]]],
                          remaining_gates: int) -> Optional[Circuit]:
        self._search_stats['nodes_explored'] += 1

        if circuit.has_all_outputs_connected() and circuit.is_functionally_correct(target_truth_table):
            return circuit

        if remaining_gates <= 0:
            return None

        if self.enable_pruning:
            missing_outputs = set(circuit.output_signals) - circuit.all_signals
            if len(missing_outputs) > remaining_gates:
                self._search_stats['nodes_pruned'] += 1
                return None

        for gate_type in self.available_gates:
            for placement in self._generate_all_placements(circuit, gate_type):
                input_signals, output_signals = placement

                new_circuit = circuit.copy()
                new_circuit.add_gate(gate_type, input_signals, output_signals)

                result = self._backtrack_search(new_circuit, target_truth_table, remaining_gates - 1)
                if result:
                    return result

        return None

    def _generate_all_placements(self, circuit: Circuit, gate_type: Gate):
        placements = []
        available_signals = list(circuit.all_signals)

        for input_combo in combinations_with_replacement(available_signals, gate_type.input_count):
            input_signals = list(input_combo)

            new_internal_signals = circuit.generate_unique_signals(gate_type.output_count)
            placements.append((input_signals, new_internal_signals))

            if gate_type.output_count == len(circuit.output_signals):
                unconnected_outputs = [sig for sig in circuit.output_signals if sig not in circuit.all_signals]
                if len(unconnected_outputs) == gate_type.output_count:
                    placements.append((input_signals, circuit.output_signals[:]))

            unconnected_outputs = [sig for sig in circuit.output_signals if sig not in circuit.all_signals]
            if len(unconnected_outputs) > 0 and gate_type.output_count == 1:
                for output_sig in unconnected_outputs:
                    output_signals = [output_sig]
                    placements.append((input_signals, output_signals))

        return placements

    def _reset_stats(self):
        self._search_stats = {'nodes_explored': 0, 'nodes_pruned': 0}
