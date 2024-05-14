from yeeducli.openapi.notebook.notebook_config import NotebookConfig
from yeeducli.openapi.notebook.notebook_instance import NotebookInstance
from yeeducli.openapi.notebook.download_notebook_instance_logs import DownloadNotebookInstanceLogs
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.json_utils import *
import sys

logger = Logger.get_logger(__name__, True)


# Notebook Job Configuration
def create_notebook_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        del json_data["workspace_id"]

        response_json, status_code = NotebookConfig.add_notebook_config(
            trim_json_data.get('workspace_id'),
            json_data
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_notebook_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookConfig.get_notebook_config_by_id_or_name(
            json_data.get('workspace_id'),
            json_data.get('notebook_conf_id'),
            json_data.get('notebook_name')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_notebook_configs(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookConfig.search_notebook_config_by_workspaceId_and_name(
            json_data.get('workspace_id'),
            json_data.get('notebook_name'),
            json_data.get('enable'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_notebook_configs(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookConfig.list_notebook_configs(
            json_data.get('workspace_id'),
            json_data.get('enable'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_notebook_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('notebook_conf_id') is not None:
            del json_data["notebook_conf_id"]
        if json_data.get('notebook_name') is not None:
            del json_data["notebook_name"]

        del json_data["workspace_id"]

        if json_data.get('name') is not None:
            json_data["notebook_name"] = json_data.get('name')
            del json_data["name"]

        response_json, status_code = NotebookConfig.edit_notebook_config(
            trim_json_data.get('workspace_id'),
            json_data,
            trim_json_data.get('notebook_conf_id'),
            trim_json_data.get('notebook_name')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def enable_notebook_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookConfig.enable_notebook_config_by_id_or_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_conf_id'),
            trim_json_data.get('notebook_name')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def disable_notebook_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookConfig.disable_notebook_config_by_id_or_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_conf_id'),
            trim_json_data.get('notebook_name')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Notebook Job Instance
def start_notebook_run(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = remove_output(args)

        del json_data["workspace_id"]

        response_json, status_code = NotebookInstance.add_notebook_instance(
            trim_json_data.get('workspace_id'),
            json_data
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def notebook_kernel_start(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookInstance.notebook_instance_kernel_start(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_id')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def notebook_kernel_interrupt(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookInstance.notebook_instance_kernel_interrupt(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_id')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def notebook_kernel_restart(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookInstance.notebook_instance_kernel_restart(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_id')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_notebook_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookInstance.get_notebook_inst_by_id(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_id')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_notebook_instances(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookInstance.search_notebook_instance_by_workspaceId_and_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_name'),
            trim_json_data.get('page_number'),
            trim_json_data.get('limit')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_notebook_instances(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookInstance.list_notebook_instances(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('cluster_id'),
            json_data.get('notebook_conf_id'),
            json_data.get('notebook_name'),
            json_data.get('notebook_status')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def stop_notebook_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NotebookInstance.stop_notebook_instance_by_id(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_id')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Download Notebook Instance Log Files
def download_notebook_instance_log_records(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = DownloadNotebookInstanceLogs.get_notebook_instance_logs(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('notebook_id'),
            trim_json_data.get('log_type')
        )

        if (response_json is not True):
            confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
