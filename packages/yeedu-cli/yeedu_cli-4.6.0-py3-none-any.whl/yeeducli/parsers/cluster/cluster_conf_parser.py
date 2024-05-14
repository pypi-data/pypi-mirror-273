from yeeducli.constants import CLOUD_PROVIDERS_LIST, COMPUTE_TYPES_LIST
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class ClusterConfigurationParser:

    def cluster_configuration_parser(subparser):

        create_cluster_conf = subparser.add_parser(
            'create-conf',
            help='To create the Cluster Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_cluster_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-conf."
        )
        create_cluster_conf.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create-conf."
        )
        create_cluster_conf.add_argument(
            "--machine_type_category_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine_category_type_id to create_cluster_conf."
        )
        create_cluster_conf.add_argument(
            "--machine_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine_type_id to create_cluster_conf."
        )
        create_cluster_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide volume_conf_id to create_cluster_conf."
        )
        create_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_cluster_conf = subparser.add_parser(
            'list-confs',
            help='To list all the available Cluster Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        list_cluster_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide specific cloud_provider_id to get information about related  Cluster Configuration."
        )
        list_cluster_conf.add_argument(
            "--compute_type",
            type=check_non_empty_string,
            nargs='?',
            choices=COMPUTE_TYPES_LIST,
            default=SUPPRESS,
            help="Provide specific compute_type to get information about related Cluster Configuration."
        )
        list_cluster_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Cluster Configuration for a specific page_number."
        )
        list_cluster_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Cluster Configuration."
        )
        list_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        search_cluster_conf = subparser.add_parser(
            'search-confs',
            help='To search all the available Cluster Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        search_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Cluster Config Name to search Cluster Configurations."
        )
        search_cluster_conf.add_argument(
            "--compute_type",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            choices=COMPUTE_TYPES_LIST,
            help="Provide specific compute type to search information about related Cluster Configuration."
        )
        search_cluster_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide specific cloud_provider_id to search information about related Cluster Configuration."
        )
        search_cluster_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Cluster Configuration for a specific page_number."
        )
        search_cluster_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Cluster Configuration."
        )
        search_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        search_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_cluster_conf = subparser.add_parser(
            'get-conf',
            help='To get the information about a specific Cluster Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_cluster_conf.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Config Id to get information about a specific Cluster Configuration."
        )
        get_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Config Name to get information about a specific Cluster Configuration."
        )
        get_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_cluster_conf = subparser.add_parser(
            'edit-conf',
            help='To edit a specific Cluster Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_cluster_conf.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific Cluster Config Id to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific Cluster Config Name to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide description to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--machine_type_category_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide machine_type_category_id to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--machine_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide machine_type_id to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide volume_conf_id to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_cluster_conf = subparser.add_parser(
            'delete-conf',
            help='To delete a specific Cluster Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_cluster_conf.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Config Id to delete a specific Cluster Configuration."
        )
        delete_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Config Name to delete a specific Cluster Configuration."
        )
        delete_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
