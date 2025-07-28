from typing import Dict, Tuple, List
from dataclasses import dataclass

@dataclass(frozen=True)
class Gate:
    name: str
    input_count: int
    output_count: int
    truth_table: Dict[Tuple[int, ...], Tuple[int, ...]]

    def __post_init__(self):
        expected_entries = 2 ** self.input_count
        if len(self.truth_table) != expected_entries:
            raise ValueError(f"Gate {self.name} truth table incomplete: expected {expected_entries}, got {len(self.truth_table)}")

@dataclass
class GateInstance:
    gate_type: Gate
    input_signals: List[str]
    output_signals: List[str]
    level: int = 0
