import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    # input_group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument("-m",
                        "--mode",
                        help="The operating mode.",
                        type=str,
                        choices=["settimeline", "gettimeline"],
                        required=True)

    parser.add_argument("-p",
                        "--project",
                        help="The name of a project",
                        type=str,
                        nargs='+',
                        default=None)

    parser.add_argument("-t",
                        "--timeline",
                        help="The name of a timeline",
                        type=str,
                        nargs='+',
                        default=None)

    parser.add_argument("-d",
                        "--database",
                        help="The database. The format is: DbName:DbType for disk driven databases and "
                             "DbName:DbType:IpAddress for PostgreSQL databases",
                        type=str,
                        nargs='+',
                        default=None)

    parser.add_argument("-o",
                        "--output-path",
                        help="The name and path of the output file. This file holds the result like timeline "
                             "attributes or error messages.",
                        type=str,
                        nargs='+',
                        required=True,
                        default=None)

    parser.add_argument("-w",
                        "--wait",
                        help="Amounts of seconds to wait between the first and second connection attempt",
                        type=int,
                        default=0)

    args = parser.parse_args()

    if args.database is not None:
        args.database = ' '.join(args.database)
    if args.project is not None:
        args.project = ' '.join(args.project)
    if args.output_path is not None:
        args.output_path = ' '.join(args.output_path)
    if args.timeline is not None:
        args.timeline = ' '.join(args.timeline)

    if args.mode == "settimeline" and (args.project is None or args.timeline is None or args.database is None):
        parser.error("-m settimeline requires -p, -t and -d argument")
    if args.mode == "gettimeline" and (args.output_path is None):
        parser.error("-m gettimeline requires -o")

    return args
