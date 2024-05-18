import argparse
import os
import sys


class GetPolicyMergeArgs:
    def __init__(self, logger=None, cmdline_arguments=None):
        self.parser = self.create_parser()
        self.logger = logger
        self.logger_info = logger
        self.logger_warning = logger
        self.logger_error = logger
        self.cmdline_arguments = cmdline_arguments
        self.set_logger(select_logger=logger)
        self.parse_args()
        self.validate_arguments()
        self.print_arguments()

    def set_logger(self, select_logger=None):
        if select_logger is None:
            self.logger = print
            self.logger_info = print
            self.logger_error = print
        else:
            self.logger = select_logger
            self.logger_info = select_logger.info
            self.logger_error = select_logger.error


    def create_parser(self):
        # Create the parser
        parser = argparse.ArgumentParser(description="Merge cids from an old policy to a new policy.",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        # Add arguments
        parser.add_argument("--new_policy_id", type=int, required=True,
                            help="The new policy id you would like to merge old cids into.")
        parser.add_argument("--old_policy_id", type=int, required=True,
                            help="The old policy id with cids you customized.")
        parser.add_argument("--cid_list", type=str, required=True,
                            help="(optional) Comma separated list of cids to move from old policy to new policy.",
                            default="")
        parser.add_argument("--storage_dir", type=str, required=True,
                            help="Directory path for storing your data, default is users home directory")
        parser.add_argument("--execute", type=str, required=True, help="Qualys tool to execute.")
        parser.add_argument("--log_to_console", action='store_true',
                            help="Send logs to console instead of file.")

        return parser


    def parse_args(self):
        # Parse the arguments
        self.args = self.parser.parse_args(self.cmdline_arguments)

    def validate_arguments(self):
        # Validate --new_policy_id and --old_policy_id are integers
        try:
            self.args.new_policy_id = int(self.args.new_policy_id)
            self.args.old_policy_id = int(self.args.old_policy_id)
        except ValueError:
            self.logger_error("Error: --new_policy_id and --old_policy_id must be integers.")
            self.parser.print_usage()
            sys.exit(1)

        # Validate --cid_list is a list of integers, if provided
        if self.args.cid_list:
            try:
                self.args.cid_list = [int(cid) for cid in self.args.cid_list.split(",")]
            except ValueError:
                self.logger_error("Error: --cid_list must be a comma separated list of integers.")
                self.parser.print_usage()
                sys.exit(1)

    def print_arguments(self):
        self.logger_info(f"New Policy ID: {self.args.new_policy_id}")
        self.logger_info(f"Old Policy ID: {self.args.old_policy_id}")
        self.logger_info(f"CID List: {self.args.cid_list if self.args.cid_list else 'None (All CIDs from the old policy will be considered)'}")


if __name__ == "__main__":
    policy_merger = GetPolicyMergeArgs(logger=None, cmdline_arguments=sys.argv)
    policy_merger20 = GetPolicyMergeArgs(logger=None,cmdline_arguments=sys.argv)
    #policy_merger.args.cid_list
