import argparse
import csv
import json


def sum_nums(args):
    print("Sum:",sum(args.numbers))


def gen(args):
    print("Generated:"," ".join([str(i) for i in (list(range(args.start,args.stop,args.step)))]))


def conv(args):
    with open(args.input) as data:
        data = json.load(data)

    with open(args.output, 'w') as file:
        writer = csv.DictWriter(file, data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():


    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(dest='command')
    sum_numbers = sub_parser.add_parser('sum', help="This function sums a list of integers")
    generator = sub_parser.add_parser('generate', help="This function generates a list of integers")
    converter = sub_parser.add_parser('convert', help="This function converts a json file to a csv file")

    sum_numbers.add_argument("numbers", type=int, nargs='+')
    sum_numbers.set_defaults(func=sum_nums)

    generator.add_argument('--start', type=int, default=0)
    generator.add_argument('--stop', type=int)
    generator.add_argument('--step', type=int, default=1)
    generator.set_defaults(func=gen)

    converter.add_argument('--input', type=str)
    converter.add_argument('--output', type=str)
    converter.set_defaults(func=conv)

    cmd = parser.parse_args()
    cmd.func(cmd)


if __name__ == '__main__':
    main()
