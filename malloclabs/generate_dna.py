"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

import argparse
import random
import sys


def DNA(length: int) -> str:
    return "".join(random.choice("ACGT") for _ in range(length))


if __name__ == "__main__":

    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(
        description="COMP3506/7505 Assignment One: Generate DNA"
    )
    parser.add_argument(
        "--number", type=int, required=True, help="Number of sequences to generate."
    )
    parser.add_argument(
        "--length", type=int, required=True, help="The length of each sequence."
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Output file to write the sequences."
    )
    args = parser.parse_args()

    # No arguments passed
    if len(sys.argv) == 0:
        parser.print_help()
        sys.exit(-1)

# Open the output file in write mode
    with open(args.output, "w") as file:
        # Generate...
        for _ in range(args.number):
            file.write(DNA(args.length) + "\n")
