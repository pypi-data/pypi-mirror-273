from argparse import ArgumentDefaultsHelpFormatter, SUPPRESS
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class UserParser:

    # 'list-tenants', 'associate-tenant', 'get-user-info', 'get-user-roles',
    def user_parser(subparser):

        list_tenants = subparser.add_parser(
            'list-tenants',
            help='To list all the available tenants for the session user.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_tenants.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list the available tenants for a specific page_number."
        )
        list_tenants.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of available tenants."
        )
        list_tenants.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_tenants.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        associate_tenant = subparser.add_parser(
            'associate-tenant',
            help="To associate the tenant with the current user's session token.",
            formatter_class=ArgumentDefaultsHelpFormatter)
        associate_tenant.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide tenant_id to associate it with session token"
        )
        associate_tenant.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        associate_tenant.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_user_info = subparser.add_parser(
            'get-user-info',
            help='To get information about current session user.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user_info.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_user_info.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_user_roles = subparser.add_parser(
            'get-user-roles',
            help='To get all the roles of current session user.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user_roles.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide tenant_id to get the user roles in that tenant."
        )
        get_user_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_user_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
