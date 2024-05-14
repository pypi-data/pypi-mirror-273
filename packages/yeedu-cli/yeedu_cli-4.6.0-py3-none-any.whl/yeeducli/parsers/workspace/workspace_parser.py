from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class WorkspaceParser:
    def workspace_parser(subparser):
        create_workspace = subparser.add_parser(
            'create',
            help='To create a Workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_workspace.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to create workspace."
        )
        create_workspace.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create workspace."
        )
        create_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_workspace = subparser.add_parser(
            'list',
            help='To list all the Workspaces.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to list Workspaces."
        )
        list_workspace.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Workspaces for a specific page_number."
        )
        list_workspace.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Workspaces."
        )
        list_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        search_workspace = subparser.add_parser(
            'search',
            help='To search workspaces by workspace name.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace name to search workspaces."
        )
        search_workspace.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to search workspaces."
        )
        search_workspace.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search workspaces for a specific page_number."
        )
        search_workspace.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of workspaces."
        )
        search_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        search_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_wokspace = subparser.add_parser(
            'get',
            help='To get information about a specific Workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_wokspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_id to get information about a specific Workspace."
        )
        get_wokspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_name to get information about a specific Workspace."
        )
        get_wokspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_wokspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_workspace = subparser.add_parser(
            'edit',
            help='To edit a specific Workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_id to edit a specific Workspace."
        )
        edit_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_name to edit a specific Workspace."
        )
        edit_workspace.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit a specific Workspace."
        )
        edit_workspace.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit a specific Workspace."
        )
        edit_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        enable_workspace = subparser.add_parser(
            'enable',
            help='To enable a specific Workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        enable_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_id to enable a specific Workspace."
        )
        enable_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_name to enable a specific Workspace."
        )
        enable_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        enable_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        disable_workspace = subparser.add_parser(
            'disable',
            help='To disable a specific Workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        disable_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_id to disable a specific Workspace."
        )
        disable_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_name to disable a specific Workspace."
        )
        disable_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        disable_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
