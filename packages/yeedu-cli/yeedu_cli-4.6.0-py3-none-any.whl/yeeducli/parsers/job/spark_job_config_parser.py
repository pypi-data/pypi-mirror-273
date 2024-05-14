from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from yeeducli.constants import JOB_TYPE_LANG
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class SparkJobConfigurationParser:

    def spark_job_configuration_parser(subparser):

        create_spark_job_conf = subparser.add_parser(
            'create-conf',
            help='To create the Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_spark_job_conf.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_id to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--files",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--properties-file",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide properties-file to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--conf",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--packages",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--repositories",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide repositories to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--jars",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--archives",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide archives to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-memory",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-memory to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-java-options",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-java-options to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-library-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-library-path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-class-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-class-path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--executor-memory",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-memory to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--total-executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide total-executor-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--num-executors",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide num-executors to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--principal",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide principal to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--keytab",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide keytab to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--queue",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide queue to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-class-name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-class-name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-command",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-command to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-arguments",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-arguments to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-raw-scala-code",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide job-raw-scala-code file path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-type",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            choices=JOB_TYPE_LANG,
            required=True,
            help="Provide job-type to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--max_concurrency",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide max_concurrency number to limit the number of jobs submitted."
        )
        create_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_spark_job_conf = subparser.add_parser(
            'list-confs',
            help='To list all the available Job Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="To list Job Configurations of a specific workspace."
        )
        list_spark_job_conf.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to list Job Configurations of a specific workspace."
        )
        list_spark_job_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Job Configurations for a specific page_number."
        )
        list_spark_job_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Job Configurations."
        )
        list_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        search_job_confs = subparser.add_parser(
            'search-confs',
            help='To search job configurations by job conf name in a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_job_confs.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to search job configurations in it."
        )
        search_job_confs.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide job_conf_name to search job configurations."
        )
        search_job_confs.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to search job configurations."
        )
        search_job_confs.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search job configurations for a specific page_number."
        )
        search_job_confs.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of job configurations."
        )
        search_job_confs.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        search_job_confs.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_spark_job_conf = subparser.add_parser(
            'get-conf',
            help='To get the information about a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to get information about a specific Spark Job Configuration."
        )
        describe_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to get information about a specific Spark Job Configuration."
        )
        describe_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config name to get information about a specific Spark Job Configuration."
        )
        describe_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_spark_job_conf = subparser.add_parser(
            'edit-conf',
            help='To edit the Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_id to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--files",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--properties-file",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide properties-file to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--conf",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--packages",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--repositories",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide repositories to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--jars",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--archives",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide archives to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-memory",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-memory to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-java-options",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-java-options to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-library-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-library-path to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-class-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-class-path to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--executor-memory",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-memory to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-cores to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--total-executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide total-executor-cores to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-cores to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--num-executors",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide num-executors to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--principal",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide principal to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--keytab",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide keytab to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--queue",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide queue to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-class-name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-class-name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-command",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-command to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-arguments",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-arguments to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-raw-scala-code",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide job-raw-scala-code file path to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--max_concurrency",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide max_concurrency number to limit the number of jobs submitted."
        )
        edit_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        enable_spark_job_conf = subparser.add_parser(
            'enable-conf',
            help='To enable a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        enable_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to enable the Spark Job Configuration."
        )
        enable_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to enable the Spark Job Configuration."
        )
        enable_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Name to enable the Spark Job Configuration."
        )
        enable_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        enable_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        disable_spark_job_conf = subparser.add_parser(
            'disable-conf',
            help='To disable a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        disable_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to disable the Spark Job Configuration."
        )
        disable_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to disable the Spark Job Configuration."
        )
        disable_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Name to disable the Spark Job Configuration."
        )
        disable_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        disable_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
