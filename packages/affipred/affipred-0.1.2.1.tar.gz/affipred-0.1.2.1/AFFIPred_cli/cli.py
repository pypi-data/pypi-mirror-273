"""
The command-line interface for AFFIPred
"""
import argparse
from .affipred import affipred


def main():
    parser = argparse.ArgumentParser(
        description="AlphaFold based Functional Impact Prediction tool for Missense Variations."
    )
    parser.add_argument(
        "input", type=str,
        help="The VCF file to calculate prediction."
    )
    parser.add_argument(
        "--output", "-o",
        help=("Name of the output file. It will be placed under the current directory.")
    )
    args = parser.parse_args()
    affipred(input_file=args.input, output_file=args.output)
    print("Success!")

if __name__ == "__main__":
    main()