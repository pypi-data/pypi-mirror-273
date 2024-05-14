from yeeducli.constants import SPARK_JOB_STATUS, SPARK_JOB_TYPE
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class SparkJobInstanceParser:
    def spark_job_parser(subparser):
        start_spark_job_run = subparser.add_parser(
            'start',
            help='To run a Spark Job Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        start_spark_job_run.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To run a Spark Job Instance, enter job_conf_id."
        )
        start_spark_job_run.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="To run a Spark Job Instance, enter job_conf_name."
        )
        start_spark_job_run.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To run a Spark Job Instance, enter workspace_id."
        )
        start_spark_job_run.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        start_spark_job_run.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_spark_job_inst = subparser.add_parser(
            'list',
            help='To list all the available Spark Job Instances.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_spark_job_inst.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To list Spark Job Instances of a specific workspace_id."
        )
        list_spark_job_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To list Spark Job Instances of a specific cluster_id."
        )
        list_spark_job_inst.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To list Spark Job Instances of a specific job_conf_id."
        )
        list_spark_job_inst.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="To list Spark Job Instances of a specific job_conf_name."
        )
        list_spark_job_inst.add_argument(
            "--job_status",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            choices=SPARK_JOB_STATUS,
            help="To list Spark Job Instances of a specific job_status."
        )
        list_spark_job_inst.add_argument(
            "--job_type",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            choices=SPARK_JOB_TYPE,
            help="To list Spark Job Instances of a specific job_type."
        )
        list_spark_job_inst.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Spark Job Instances for a specific page_number."
        )
        list_spark_job_inst.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of job instances."
        )
        list_spark_job_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_spark_job_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        search_job_inst = subparser.add_parser(
            'search',
            help='To search Spark Job Instances by similar job id.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_job_inst.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to search Spark Job Instances in it."
        )
        search_job_inst.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To search Spark Job Instances of a specific job_conf_name."
        )
        search_job_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To search Spark Job Instances of a specific cluster_id."
        )
        search_job_inst.add_argument(
            "--job_status",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            choices=SPARK_JOB_STATUS,
            help="To search Spark Job Instances of a specific job_status."
        )
        search_job_inst.add_argument(
            "--job_type",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            choices=SPARK_JOB_TYPE,
            help="To search Spark Job Instances of a specific job_type."
        )
        search_job_inst.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Spark Job Instances for a specific page_number."
        )
        search_job_inst.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Spark Job Instances."
        )
        search_job_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        search_job_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_job_instance = subparser.add_parser(
            'get',
            help='To get information about a specific Spark Job Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_job_instance.add_argument(
            "--job_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide job_id to get information about a specific Spark Job Instance."
        )
        get_job_instance.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to get information about a specific Spark Job Instance."
        )
        get_job_instance.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_job_instance.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        stop_spark_job_inst = subparser.add_parser(
            'stop',
            help='To stop a specific Spark Job Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        stop_spark_job_inst.add_argument(
            "--job_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide job_id to stop a specific Spark Job Instance."
        )
        stop_spark_job_inst.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to stop a specific Spark Job Instance."
        )
        stop_spark_job_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        stop_spark_job_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_workflow_job_inst = subparser.add_parser(
            'get-workflow-job-instance',
            help='To get information about a specific Workflow Job Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_workflow_job_inst.add_argument(
            "--job_application_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide a job_application_id to get information about a specific Workflow Job Instance."
        )
        get_workflow_job_inst.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide a workspace_id to get information about a specific Workflow Job Instance."
        )
        get_workflow_job_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_workflow_job_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_job_instance_status = subparser.add_parser(
            'get-status',
            help='To get all the status information about a specific Spark Job Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_job_instance_status.add_argument(
            "--job_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide job_id to get all the status information about a specific Spark Job Instance."
        )
        get_job_instance_status.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to get all the status information about a specific Spark Job Instance."
        )
        get_job_instance_status.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_job_instance_status.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
