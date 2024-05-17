import argparse

import solidipes.reports
from solidipes.reports.report import Report
from solidipes.utils.list_subclasses import get_subclasses_from_package

# from solidipes.utils import mount_all

command = "report"
command_help = "Generate a report or launch a report interface for the given directory."


# Get all report makers
report_subclasses = get_subclasses_from_package(solidipes.reports, Report, "report")
report_subclasses_instances = [Subclass() for Subclass in report_subclasses]
reports = {report.command: report for report in report_subclasses_instances}


def main(args):
    report_type = args.report_type
    report = reports[report_type]
    # mount_all(headless=True)
    report.make(args)


def populate_arg_parser(parser):
    # Create subparsers for each report type
    report_parsers = parser.add_subparsers(dest="report_type", help="Type of report to generate")
    report_parsers.required = True

    for report in reports.values():
        uploader_parser = report_parsers.add_parser(report.command, help=report.command_help)
        report.populate_arg_parser(uploader_parser)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    populate_arg_parser(parser)
    args = parser.parse_args()
    main(args)
