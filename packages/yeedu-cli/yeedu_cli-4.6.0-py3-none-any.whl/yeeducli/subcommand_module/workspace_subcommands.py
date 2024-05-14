from yeeducli.openapi.workspace.workspace import Workspace
from yeeducli.openapi.workspace.workspace_access_control import WorkspaceAccessControl
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.json_utils import *
import sys

logger = Logger.get_logger(__name__, True)


# Workspace
def create_workspace(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = Workspace.create_workspace(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = Workspace.get_workspace_by_id_or_name(
            json_data.get('workspace_id'),
            json_data.get('workspace_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = Workspace.search_workspace_by_name(
            json_data.get('workspace_name'),
            json_data.get('enable'),
            json_data.get('page_number'),
            json_data.get('limit')
        )

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspaces(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = Workspace.list_workspaces(
            json_data.get('enable'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_workspace(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('workspace_id') is not None:
            del json_data["workspace_id"]
        if json_data.get('workspace_name') is not None:
            del json_data["workspace_name"]

        response_json, status_code = Workspace.edit_workspace_by_id_or_name(
            json_data,
            trim_json_data.get('workspace_id'),
            trim_json_data.get('workspace_name')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def enable_workspace(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = Workspace.enable_workspace_by_id_or_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('workspace_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def disable_workspace(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = Workspace.disable_workspace_by_id_or_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('workspace_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Workspace Access Control
def create_workspace_user_access(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        del json_data["workspace_id"]

        response_json, status_code = WorkspaceAccessControl.create_workspace_user_access(
            trim_json_data.get('workspace_id')[0],
            json_data
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def create_workspace_group_access(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        del json_data["workspace_id"]

        response_json, status_code = WorkspaceAccessControl.create_workspace_group_access(
            trim_json_data.get('workspace_id')[0],
            json_data
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_workspace_user_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.delete_workspace_user_access(
            json_data.get('workspace_id'),
            json_data.get('user_id'),
            json_data.get('permission_id')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_workspace_group_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.delete_workspace_group_access(
            json_data.get('workspace_id'),
            json_data.get('group_id'),
            json_data.get('permission_id')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.list_workspace_users(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('group_id')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_users_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.list_workspace_users_access(
            json_data.get('workspace_id'),
            json_data.get('permission_id'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.search_workspace_users(
            json_data.get('workspace_id'),
            json_data.get('username'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('group_id')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def match_workspace_user(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.match_workspace_user(
            json_data.get('workspace_id'),
            json_data.get('username')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.list_workspace_groups(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('user_id')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_groups_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.list_workspace_groups_access(
            json_data.get('workspace_id'),
            json_data.get('permission_id'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.search_workspace_groups(
            json_data.get('workspace_id'),
            json_data.get('groupname'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('user_id')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def match_workspace_group(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.match_workspace_group(
            json_data.get('workspace_id'),
            json_data.get('groupname')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace_user_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.get_workspace_user_access(
            json_data.get('workspace_id'),
            json_data.get('user_id')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace_group_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = WorkspaceAccessControl.get_workspace_group_access(
            json_data.get('workspace_id'),
            json_data.get('group_id')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
