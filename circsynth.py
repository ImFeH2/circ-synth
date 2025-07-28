#!/usr/bin/env python3
"""
CircSynth - Circuit Synthesis Tool
Author: ImFeH2 <i@feh2.im>

Standalone script launcher
"""

import sys
import os
import argparse

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from examples.basic import run_xor_synthesis, run_majority_function, \
    run_majority_with_maj3
from examples.full_adder import run_full_adder_synthesis, run_sum_only, \
    run_carry_only
from examples.custom import run_custom_synthesis


def run_examples(args):
    example_map = {'xor': run_xor_synthesis, 'majority': run_majority_function,
        'majority_maj3': run_majority_with_maj3,
        'full_adder': run_full_adder_synthesis, 'full_adder_sum': run_sum_only,
        'full_adder_carry': run_carry_only, 'custom': run_custom_synthesis}

    if args.example == 'all':
        for name, func in example_map.items():
            if name != 'custom':
                try:
                    func()
                except KeyboardInterrupt:
                    print(f"\nInterrupted during {name} example")
                    sys.exit(1)
                except Exception as e:
                    print(f"Error in {name} example: {e}")
    else:
        if args.example in example_map:
            try:
                example_map[args.example]()
            except KeyboardInterrupt:
                print(f"\nInterrupted during {args.example} example")
                sys.exit(1)
            except Exception as e:
                print(f"Error in {args.example} example: {e}")
        else:
            print(f"Unknown example: {args.example}")
            sys.exit(1)


def run_interactive_mode():
    print("CircSynth Interactive Mode")
    print("==========================")
    print("Enter truth table data for synthesis")
    print("Type 'quit' to exit\n")

    try:
        num_inputs = int(input("Number of inputs: "))
        num_outputs = int(input("Number of outputs: "))

        input_names = []
        for i in range(num_inputs):
            name = input(f"Input {i + 1} name: ").strip()
            input_names.append(name)

        output_names = []
        for i in range(num_outputs):
            name = input(f"Output {i + 1} name: ").strip()
            output_names.append(name)

        print(f"\nEnter {2 ** num_inputs} truth table rows:")
        print("Format: input1,input2,... -> output1,output2,...")

        truth_data = []
        for i in range(2 ** num_inputs):
            row_input = input(f"Row {i + 1}: ").strip()
            if row_input.lower() == 'quit':
                return

            try:
                parts = row_input.split('->')
                inputs = [int(x.strip()) for x in parts[0].split(',')]
                outputs = [int(x.strip()) for x in parts[1].split(',')]
                truth_data.append((tuple(inputs), tuple(outputs)))
            except (ValueError, IndexError):
                print("Invalid format. Try again.")
                return

        from examples.custom import create_custom_example
        from gates.standard import NOT, AND, OR, XOR, NAND, NOR

        available_gates = [NOT, AND, OR, XOR, NAND, NOR]

        result = create_custom_example(truth_data, input_names, output_names,
            available_gates, max_gates=15)

        if result:
            print("\nSynthesis successful:")
            print(result)
        else:
            print("\nNo solution found")

    except KeyboardInterrupt:
        print("\nExiting interactive mode")
    except Exception as e:
        print(f"Error in interactive mode: {e}")


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    parser = argparse.ArgumentParser(
        description='CircSynth - Exact Logic Circuit Synthesis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog='''
Examples:
  python circsynth.py --example xor          # Run XOR synthesis only
  python circsynth.py --example majority     # Run majority function
  python circsynth.py --example full_adder   # Run full adder synthesis
  python circsynth.py --example all          # Run all examples
  python circsynth.py --interactive          # Interactive mode
        ''')

    parser.add_argument('--example',
        choices=['xor', 'majority', 'majority_maj3', 'full_adder',
                 'full_adder_sum', 'full_adder_carry', 'custom', 'all'],
        help='Run specific example')

    parser.add_argument('--max-gates', type=int, default=15,
        help='Maximum number of gates to try (default: 15)')

    parser.add_argument('--no-pruning', action='store_true',
        help='Disable search pruning (slower but more thorough)')

    parser.add_argument('--interactive', action='store_true',
        help='Run in interactive mode for custom truth tables')

    parser.add_argument('--version', action='version',
        version='CircSynth 1.0.0')

    args = parser.parse_args()

    if args.interactive:
        run_interactive_mode()
    elif args.example:
        run_examples(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
