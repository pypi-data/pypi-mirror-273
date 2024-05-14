from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class DownloadClusterInstanceLogParser:

    def download_cluster_instance_log_parser(subparser):

        download_cluster_instance_logs = subparser.add_parser(
            'logs',
            help='To download Cluster Instance logs for a specific Cluster Instance',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        download_cluster_instance_logs.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Id to download log records."
        )
        download_cluster_instance_logs.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Name to download log records."
        )
        download_cluster_instance_logs.add_argument(
            "--log_type",
            type=check_non_empty_string,
            nargs=1,
            default='stdout',
            choices=['stdout', 'stderr'],
            help="Provide log_type to download Cluster Instance log records."
        )
        download_cluster_instance_logs.add_argument(
            "--cluster_status_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Status Id to download log records."
        )
        download_cluster_instance_logs.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        download_cluster_instance_logs.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
