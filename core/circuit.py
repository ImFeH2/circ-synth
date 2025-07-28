from typing import Dict, List, Tuple, Optional, Set
from .gate import Gate, GateInstance

class Circuit:
    def __init__(self, input_signals: List[str], output_signals: List[str]):
        self.input_signals = input_signals[:]
        self.output_signals = output_signals[:]
        self.gate_instances: List[GateInstance] = []
        self.all_signals: Set[str] = set(input_signals)
        self._signal_counter = 0
        self._levels_computed = False

    def add_gate(self, gate_type: Gate, input_sigs: List[str], output_sigs: List[str]) -> None:
        gate_instance = GateInstance(gate_type, input_sigs[:], output_sigs[:])
        self.gate_instances.append(gate_instance)
        self.all_signals.update(output_sigs)
        self._levels_computed = False

    def generate_unique_signals(self, count: int) -> List[str]:
        signals = []
        for _ in range(count):
            signal_name = f"_s{self._signal_counter}"
            signals.append(signal_name)
            self._signal_counter += 1
        return signals

    def _compute_levels(self):
        if self._levels_computed:
            return

        signal_levels = {sig: 0 for sig in self.input_signals}

        changed = True
        while changed:
            changed = False
            for gate in self.gate_instances:
                max_input_level = 0
                all_inputs_have_level = True

                for input_sig in gate.input_signals:
                    if input_sig in signal_levels:
                        max_input_level = max(max_input_level, signal_levels[input_sig])
                    else:
                        all_inputs_have_level = False
                        break

                if all_inputs_have_level:
                    gate_level = max_input_level + 1
                    if gate.level != gate_level:
                        gate.level = gate_level
                        changed = True

                    for output_sig in gate.output_signals:
                        signal_levels[output_sig] = gate_level

        self._levels_computed = True

    def get_gates_by_level(self) -> Dict[int, List[GateInstance]]:
        self._compute_levels()
        levels = {}
        for gate in self.gate_instances:
            if gate.level not in levels:
                levels[gate.level] = []
            levels[gate.level].append(gate)
        return levels

    def evaluate(self, input_values: Tuple[int, ...]) -> Optional[Tuple[int, ...]]:
        if len(input_values) != len(self.input_signals):
            return None

        signal_values = dict(zip(self.input_signals, input_values))

        levels = self.get_gates_by_level()
        for level in sorted(levels.keys()):
            for gate_instance in levels[level]:
                input_vals = []
                for sig in gate_instance.input_signals:
                    if sig not in signal_values:
                        return None
                    input_vals.append(signal_values[sig])

                input_tuple = tuple(input_vals)
                if input_tuple not in gate_instance.gate_type.truth_table:
                    return None

                output_vals = gate_instance.gate_type.truth_table[input_tuple]

                for sig, val in zip(gate_instance.output_signals, output_vals):
                    signal_values[sig] = val

        result = []
        for sig in self.output_signals:
            if sig not in signal_values:
                return None
            result.append(signal_values[sig])

        return tuple(result)

    def is_functionally_correct(self, target_truth_table: List[Tuple[Tuple[int, ...], Tuple[int, ...]]]) -> bool:
        for input_vals, expected_output_vals in target_truth_table:
            actual_output = self.evaluate(input_vals)
            if actual_output != expected_output_vals:
                return False
        return True

    def has_all_outputs_connected(self) -> bool:
        return all(output in self.all_signals for output in self.output_signals)

    def gate_count(self) -> int:
        return len(self.gate_instances)

    def copy(self) -> 'Circuit':
        new_circuit = Circuit(self.input_signals[:], self.output_signals[:])
        new_circuit.gate_instances = [
            GateInstance(gi.gate_type, gi.input_signals[:], gi.output_signals[:], gi.level)
            for gi in self.gate_instances
        ]
        new_circuit.all_signals = self.all_signals.copy()
        new_circuit._signal_counter = self._signal_counter
        return new_circuit

    def to_graphviz(self) -> str:
        self._compute_levels()

        dot = ["digraph Circuit {"]
        dot.append("    rankdir=LR;")
        dot.append("    node [shape=box];")

        levels = self.get_gates_by_level()

        dot.append("    subgraph cluster_inputs {")
        dot.append("        label=\"Inputs\";")
        dot.append("        style=dashed;")
        for inp in self.input_signals:
            dot.append(f"        \"{inp}\" [shape=ellipse, style=filled, fillcolor=lightblue];")
        dot.append("    }")

        dot.append("    subgraph cluster_outputs {")
        dot.append("        label=\"Outputs\";")
        dot.append("        style=dashed;")
        for out in self.output_signals:
            dot.append(f"        \"{out}\" [shape=ellipse, style=filled, fillcolor=lightgreen];")
        dot.append("    }")

        for level in sorted(levels.keys()):
            dot.append(f"    subgraph cluster_level_{level} {{")
            dot.append(f"        label=\"Level {level}\";")
            dot.append("        style=dashed;")

            for i, gate in enumerate(levels[level]):
                gate_id = f"gate_{level}_{i}"
                dot.append(f"        \"{gate_id}\" [label=\"{gate.gate_type.name}\", style=filled, fillcolor=lightyellow];")

                for input_sig in gate.input_signals:
                    if input_sig in self.input_signals or any(input_sig in g.output_signals for g in self.gate_instances):
                        dot.append(f"    \"{input_sig}\" -> \"{gate_id}\";")

                for output_sig in gate.output_signals:
                    dot.append(f"    \"{gate_id}\" -> \"{output_sig}\";")

            dot.append("    }")

        dot.append("}")
        return "\n".join(dot)

    def __str__(self) -> str:
        self._compute_levels()
        levels = self.get_gates_by_level()

        lines = [f"Circuit: {self.input_signals} -> {self.output_signals}"]
        lines.append(f"Total gates: {self.gate_count()}")
        lines.append("")

        for level in sorted(levels.keys()):
            lines.append(f"Level {level}:")
            for i, gate in enumerate(levels[level]):
                gate_name = f"  Gate {level}.{i}"
                gate_desc = f"{gate.gate_type.name}({', '.join(gate.input_signals)}) -> {', '.join(gate.output_signals)}"
                lines.append(f"{gate_name}: {gate_desc}")
            lines.append("")

        return '\n'.join(lines)
