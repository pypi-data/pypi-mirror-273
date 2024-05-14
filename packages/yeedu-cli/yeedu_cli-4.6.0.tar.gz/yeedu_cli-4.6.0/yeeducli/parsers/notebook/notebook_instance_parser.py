from yeeducli.constants import SPARK_JOB_STATUS
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class NotebookInstanceParser:
    def notebook_instance_parser(subparser):
        start_notebook_instance = subparser.add_parser(
            'start',
            help='To start a Notebook Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        start_notebook_instance.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To start a Notebook Instance, enter workspace_id."
        )
        start_notebook_instance.add_argument(
            "--notebook_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To start a Notebook Instance, enter notebook_conf_id."
        )
        start_notebook_instance.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="To start a Notebook Instance, enter notebook_name."
        )
        start_notebook_instance.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        start_notebook_instance.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        notebook_instance_kernel_start = subparser.add_parser(
            'kernel-start',
            help='To start a kernel of a Notebook Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        notebook_instance_kernel_start.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To start a kernel of a Notebook Instance, enter workspace_id."
        )
        notebook_instance_kernel_start.add_argument(
            "--notebook_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To start a kernel of a Notebook Instance, enter notebook instance id."
        )
        notebook_instance_kernel_start.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        notebook_instance_kernel_start.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        notebook_instance_kernel_interrupt = subparser.add_parser(
            'kernel-interrupt',
            help='To interrupt a kernel of a Notebook Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        notebook_instance_kernel_interrupt.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To interrupt a kernel of a Notebook Instance, enter workspace_id."
        )
        notebook_instance_kernel_interrupt.add_argument(
            "--notebook_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To interrupt a kernel of a Notebook Instance, enter notebook instance id."
        )
        notebook_instance_kernel_interrupt.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        notebook_instance_kernel_interrupt.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        notebook_instance_kernel_restart = subparser.add_parser(
            'kernel-restart',
            help='To restart a kernel of a Notebook Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        notebook_instance_kernel_restart.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To restart a kernel of a Notebook Instance, enter workspace_id."
        )
        notebook_instance_kernel_restart.add_argument(
            "--notebook_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To restart a kernel of a Notebook Instance, enter notebook instance id."
        )
        notebook_instance_kernel_restart.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        notebook_instance_kernel_restart.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_notebook_instances = subparser.add_parser(
            'list',
            help='To list all the available Notebook Instances.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_notebook_instances.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To list Notebook Instances of a specific workspace_id."
        )
        list_notebook_instances.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To list Notebook Instances of a specific cluster_id."
        )
        list_notebook_instances.add_argument(
            "--notebook_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To list Notebook Instances of a specific notebook_conf_id."
        )
        list_notebook_instances.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="To list Notebook Instances of a specific notebook_name."
        )
        list_notebook_instances.add_argument(
            "--notebook_status",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            choices=SPARK_JOB_STATUS,
            help="To list Notebook Instances of a specific notebook_status."
        )
        list_notebook_instances.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Notebook Instances for a specific page_number."
        )
        list_notebook_instances.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of job instances."
        )
        list_notebook_instances.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_notebook_instances.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        search_notebook_instances = subparser.add_parser(
            'search',
            help='To search Notebook Instances by similar notebook name.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_notebook_instances.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to search Notebook Instances in it."
        )
        search_notebook_instances.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide notebook_name to search Notebook Instances."
        )
        search_notebook_instances.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Notebook Instances for a specific page_number."
        )
        search_notebook_instances.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Notebook Instances."
        )
        search_notebook_instances.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        search_notebook_instances.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_notebook_instance = subparser.add_parser(
            'get',
            help='To get information about a specific Notebook Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_notebook_instance.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to get information about a specific Notebook Instance."
        )
        get_notebook_instance.add_argument(
            "--notebook_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide notebook instance id to get information about a specific Notebook Instance."
        )
        get_notebook_instance.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_notebook_instance.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        stop_notebook_instance = subparser.add_parser(
            'stop',
            help='To stop a specific Notebook Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        stop_notebook_instance.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to stop a specific Notebook Instance."
        )
        stop_notebook_instance.add_argument(
            "--notebook_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide notebook instance id to stop a specific Notebook Instance."
        )
        stop_notebook_instance.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        stop_notebook_instance.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
