from core import TruthTable
from synthesis import ExactCircuitSynthesis
from gates.standard import NAND, AND, OR, MAJ3

def run_xor_synthesis():
    print("=== XOR Synthesis Example ===")

    available_gates = [NAND]

    xor_table = TruthTable(['A', 'B'], ['Y'])
    xor_table.add_row(A=0, B=0, Y=0)
    xor_table.add_row(A=0, B=1, Y=1)
    xor_table.add_row(A=1, B=0, Y=1)
    xor_table.add_row(A=1, B=1, Y=0)
    xor_truth_table = xor_table.build()

    synthesizer = ExactCircuitSynthesis(available_gates, max_gates=10)

    result = synthesizer.synthesize(
        xor_truth_table,
        input_names=['A', 'B'],
        output_names=['Y']
    )

    if result:
        print("Successfully found XOR implementation:")
        print(result)

        print("Graphviz DOT format:")
        print(result.to_graphviz())

        print("\nVerification:")
        for inputs, expected_output in xor_truth_table:
            actual_output = result.evaluate(inputs)
            status = "✓" if actual_output == expected_output else "✗"
            print(f"Input {inputs}: expected {expected_output}, actual {actual_output} {status}")
    else:
        print("No solution found")

def run_majority_function():
    print("\n=== Majority Function Synthesis Example ===")

    available_gates = [AND, OR]

    def majority_function(A, B, C):
        return int((A + B + C) >= 2)

    majority_truth_table = TruthTable.from_function(['A', 'B', 'C'], ['Y'], majority_function)

    print("Majority function truth table:")
    for inputs, outputs in majority_truth_table:
        print(f"  A={inputs[0]}, B={inputs[1]}, C={inputs[2]} -> Y={outputs[0]}")
    print()

    synthesizer = ExactCircuitSynthesis(available_gates, max_gates=6)

    result = synthesizer.synthesize(
        majority_truth_table,
        input_names=['A', 'B', 'C'],
        output_names=['Y']
    )

    if result:
        print("Successfully found majority function implementation:")
        print(result)

        print("Verification:")
        for inputs, expected_output in majority_truth_table:
            actual_output = result.evaluate(inputs)
            status = "✓" if actual_output == expected_output else "✗"
            print(f"Input {inputs}: expected {expected_output}, actual {actual_output} {status}")
    else:
        print("No solution found")

def run_majority_with_maj3():
    print("\n=== Majority Function with MAJ3 Gate ===")

    available_gates = [MAJ3]

    def majority_function(A, B, C):
        return int((A + B + C) >= 2)

    majority_truth_table = TruthTable.from_function(['A', 'B', 'C'], ['Y'], majority_function)

    synthesizer = ExactCircuitSynthesis(available_gates, max_gates=2)

    result = synthesizer.synthesize(
        majority_truth_table,
        input_names=['A', 'B', 'C'],
        output_names=['Y']
    )

    if result:
        print("Successfully found majority function with MAJ3:")
        print(result)
        print("Note: Should require only 1 MAJ3 gate!")
    else:
        print("No solution found")
