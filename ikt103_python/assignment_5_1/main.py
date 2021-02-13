import argparse
import csv
import json


def main():

    commands = argparse.ArgumentParser()
    sub_parser = commands.add_subparsers(dest='command')
    sum_numbers = sub_parser.add_parser('sum', help="This function sums a list of integers")
    generator = sub_parser.add_parser('generate', help="This function generates a list of integers")
    converter = sub_parser.add_parser('convert', help="This function converts a json file to a csv file")

    sum_numbers.add_argument("sum", type=int, nargs='+')

    generator.add_argument('--start', type=int, default=0)
    generator.add_argument('--stop', type=int)
    generator.add_argument('--step', type=int, default=1)

    converter.add_argument('--input', type=str)
    converter.add_argument('--output', type=str)

    cmd = commands.parse_args()

    if cmd.command == "sum":
        print("Sum:", sum(cmd.sum))
    elif cmd.command == "generate":
        print("Generated:", " ".join([str(i) for i in range(cmd.start, cmd.stop, cmd.step)]))
    else:
        with open(cmd.input) as data:
            data = json.load(data)

        with open(cmd.output, 'w') as file:
            writer = csv.DictWriter(file, data[0].keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)


if __name__ == '__main__':
    main()
