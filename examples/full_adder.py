from core import TruthTable
from synthesis import ExactCircuitSynthesis
from gates.standard import XOR, AND, OR

def run_full_adder_synthesis():
    print("\n=== Full Adder Synthesis Example ===")

    available_gates = [XOR, AND, OR]

    def full_adder_func(A, B, CIN):
        sum_out = A ^ B ^ CIN
        carry_out = (A & B) | (CIN & (A ^ B))
        return [sum_out, carry_out]

    full_adder_truth_table = TruthTable.from_function(
        ['A', 'B', 'CIN'],
        ['SUM', 'CARRY'],
        full_adder_func
    )

    print("Full adder truth table:")
    for inputs, outputs in full_adder_truth_table:
        print(f"  A={inputs[0]}, B={inputs[1]}, CIN={inputs[2]} -> SUM={outputs[0]}, CARRY={outputs[1]}")
    print()

    synthesizer = ExactCircuitSynthesis(available_gates, max_gates=8)

    result = synthesizer.synthesize(
        full_adder_truth_table,
        input_names=['A', 'B', 'CIN'],
        output_names=['SUM', 'CARRY']
    )

    if result:
        print("Successfully found full adder implementation:")
        print(result)

        print("Graphviz DOT format:")
        print(result.to_graphviz())

        print("\nVerification:")
        for inputs, expected_output in full_adder_truth_table[:4]:
            actual_output = result.evaluate(inputs)
            status = "✓" if actual_output == expected_output else "✗"
            print(f"Input {inputs}: expected {expected_output}, actual {actual_output} {status}")
        print("...")
    else:
        print("No solution found")

def run_sum_only():
    print("\n=== Full Adder SUM Only Synthesis Example ===")

    available_gates = [XOR, AND, OR]

    def sum_func(A, B, CIN):
        return A ^ B ^ CIN

    sum_truth_table = TruthTable.from_function(
        ['A', 'B', 'CIN'],
        ['SUM'],
        sum_func
    )

    print("Full adder SUM truth table:")
    for inputs, outputs in sum_truth_table:
        print(f"  A={inputs[0]}, B={inputs[1]}, CIN={inputs[2]} -> SUM={outputs[0]}")
    print()

    synthesizer = ExactCircuitSynthesis(available_gates, max_gates=6)

    result = synthesizer.synthesize(
        sum_truth_table,
        input_names=['A', 'B', 'CIN'],
        output_names=['SUM']
    )

    if result:
        print("Successfully found full adder SUM implementation:")
        print(result)

        print("Graphviz DOT format:")
        print(result.to_graphviz())

        print("\nVerification:")
        for inputs, expected_output in sum_truth_table:
            actual_output = result.evaluate(inputs)
            status = "✓" if actual_output == expected_output else "✗"
            print(f"Input {inputs}: expected {expected_output}, actual {actual_output} {status}")
    else:
        print("No solution found")

def run_carry_only():
    print("\n=== Full Adder CARRY Only Synthesis Example ===")

    available_gates = [XOR, AND, OR]

    def carry_func(A, B, CIN):
        return (A & B) | (CIN & (A ^ B))

    carry_truth_table = TruthTable.from_function(
        ['A', 'B', 'CIN'],
        ['CARRY'],
        carry_func
    )

    print("Full adder CARRY truth table:")
    for inputs, outputs in carry_truth_table:
        print(f"  A={inputs[0]}, B={inputs[1]}, CIN={inputs[2]} -> CARRY={outputs[0]}")
    print()

    synthesizer = ExactCircuitSynthesis(available_gates, max_gates=6)

    result = synthesizer.synthesize(
        carry_truth_table,
        input_names=['A', 'B', 'CIN'],
        output_names=['CARRY']
    )

    if result:
        print("Successfully found full adder CARRY implementation:")
        print(result)

        print("Graphviz DOT format:")
        print(result.to_graphviz())

        print("\nVerification:")
        for inputs, expected_output in carry_truth_table:
            actual_output = result.evaluate(inputs)
            status = "✓" if actual_output == expected_output else "✗"
            print(f"Input {inputs}: expected {expected_output}, actual {actual_output} {status}")
    else:
        print("No solution found")
