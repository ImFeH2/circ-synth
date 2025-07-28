from typing import List, Tuple, Callable

class TruthTable:
    def __init__(self, inputs: List[str], outputs: List[str]):
        self.inputs = inputs
        self.outputs = outputs
        self.rows = []

    def add_row(self, **kwargs):
        input_values = []
        for inp in self.inputs:
            if inp not in kwargs:
                raise ValueError(f"Missing input {inp}")
            input_values.append(kwargs[inp])

        output_values = []
        for out in self.outputs:
            if out not in kwargs:
                raise ValueError(f"Missing output {out}")
            output_values.append(kwargs[out])

        self.rows.append((tuple(input_values), tuple(output_values)))
        return self

    def build(self) -> List[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
        expected_rows = 2 ** len(self.inputs)
        if len(self.rows) != expected_rows:
            raise ValueError(f"Truth table incomplete: expected {expected_rows} rows, got {len(self.rows)}")
        return self.rows

    @staticmethod
    def from_function(inputs: List[str], outputs: List[str], func: Callable) -> List[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
        table = TruthTable(inputs, outputs)
        n_inputs = len(inputs)

        for i in range(2 ** n_inputs):
            input_vals = [(i >> j) & 1 for j in range(n_inputs)]
            input_dict = dict(zip(inputs, input_vals))

            output_vals = func(**input_dict)

            if not isinstance(output_vals, (list, tuple)):
                output_vals = [output_vals]

            output_dict = dict(zip(outputs, output_vals))
            table.add_row(**input_dict, **output_dict)

        return table.build()
