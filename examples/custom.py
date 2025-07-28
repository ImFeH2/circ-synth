from core import TruthTable
from synthesis import ExactCircuitSynthesis
from gates.standard import NOT, AND, OR, XOR, NAND, NOR

def run_custom_synthesis():
    print("\n=== Custom Truth Table Example ===")

    table = TruthTable(['A', 'B'], ['Y'])
    table.add_row(A=0, B=0, Y=1)
    table.add_row(A=0, B=1, Y=0)
    table.add_row(A=1, B=0, Y=0)
    table.add_row(A=1, B=1, Y=1)

    custom_truth_table = table.build()

    print("Custom truth table:")
    for inputs, outputs in custom_truth_table:
        print(f"  Input {inputs} -> Output {outputs}")

def create_custom_example(truth_table_data, input_names, output_names, available_gates, max_gates=10):
    table = TruthTable(input_names, output_names)

    for row in truth_table_data:
        input_dict = dict(zip(input_names, row[0]))
        output_dict = dict(zip(output_names, row[1]))
        table.add_row(**input_dict, **output_dict)

    truth_table = table.build()

    synthesizer = ExactCircuitSynthesis(available_gates, max_gates=max_gates)

    result = synthesizer.synthesize(
        truth_table,
        input_names=input_names,
        output_names=output_names
    )

    return result

def example_usage():
    truth_data = [
        ((0, 0), (1,)),
        ((0, 1), (0,)),
        ((1, 0), (0,)),
        ((1, 1), (1,))
    ]

    result = create_custom_example(
        truth_data,
        input_names=['A', 'B'],
        output_names=['Y'],
        available_gates=[AND, OR, NOT],
        max_gates=5
    )

    if result:
        print("Custom synthesis successful:")
        print(result)
    else:
        print("No solution found for custom example")
