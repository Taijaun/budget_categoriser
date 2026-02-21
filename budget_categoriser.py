import argparse
import csv
from utils import parse_amount

def build_parser():

    parser = argparse.ArgumentParser(
        description="Generate a CSV budget report from a text file of categories and amounts (one per line)."
    )

    parser.add_argument(
        "input_file",
        nargs="?",
        default="spend.txt",
        help="Path to input .txt file (default: spend.txt)"
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on the first invalid entry instead of skipping it."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test mode that disables writing to a csv."
    )

    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Path to output CSV file (default: <input>_report.csv)"
    )

    return parser

def output_filename_for(input_file: str) -> str:
    base = input_file.rsplit(".", 1)[0]
    return base + "_report.csv"

def main():
    parser = build_parser()
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output if args.output else output_filename_for(input_file)

    totals = {}

    try:
        with open(input_file, "r") as file:

            for lineno, line in enumerate(file, start=1):
                # If the line is blank or whitespace, skip it
                if not line.strip():
                    continue

                parts = line.split(",", 1)

                if len(parts) != 2:
                    if args.strict:
                        raise SystemExit(1)
                    else:
                        print(f"Invalid format (expected category, amount): {repr(lineno)}")
                        continue 

                category = parts[0].strip().lower()

                if not category:
                    if args.strict:
                        print(f"Missing category: {repr(lineno)}")
                        raise SystemExit(1)
                    else:
                        print(f"Missing category: {lineno}")
                        continue

                amount = parts[1].strip()        
                value = parse_amount(amount, args.strict)

                if value is None:
                    continue

                if category not in totals:
                    totals[category] = 0

                totals[category] += value

    except FileNotFoundError:
        print(f"File not found: {input_file}")
        raise SystemExit(1)
    
    if not totals:
        print("No valid spending data found.")
        raise SystemExit(1)
    
    grand_total = sum(totals.values())

    if args.dry_run:
        print(f"Grand total of expenses: {grand_total}")
        for category, total in totals.items():
            print(f"{category}: {total}")
        print("Dry run completed")
        return

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "total"])
        for category, total in totals.items():
            writer.writerow([category, total])
        writer.writerow(["grand_total", grand_total])

        print(f"Wrote report: {output_file}")

if __name__ == "__main__":
    main()


