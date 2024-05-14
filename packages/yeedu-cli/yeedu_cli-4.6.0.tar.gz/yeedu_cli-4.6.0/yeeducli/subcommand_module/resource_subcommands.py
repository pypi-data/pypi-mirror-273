from yeeducli.openapi.resource.boot_disk_image_configuration import BootDiskImageConfiguration
from yeeducli.openapi.resource.volume_configuration import VolumeConfiguration
from yeeducli.openapi.resource.network_configuration import NetworkConfiguration
from yeeducli.openapi.resource.cloud_environment import CloudEnvironment
from yeeducli.openapi.resource.credentials_config import CredentialsConfig
from yeeducli.openapi.resource.object_storage_manager import ObjectStorageManager
from yeeducli.openapi.resource.object_storage_manager_files import ObjectStorageManagerFiles
from yeeducli.openapi.resource.hive_metastore_configuration import HiveMetastoreConfiguration
from yeeducli.openapi.resource.lookup import Lookup
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
import json
import sys

logger = Logger.get_logger(__name__, True)


# Cloud Provider
def list_providers(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_providers()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_provider(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_provider_by_id(
            json_data.get('cloud_provider_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_az_by_provider_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = Lookup.get_az_by_provider_id(
            json_data.get('cloud_provider_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_az_by_provider_id_and_zone_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = Lookup.get_az_by_provider_id_and_zone_id(
            json_data.get('cloud_provider_id')[0], json_data.get('availability_zone_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_machine_type_by_provider_id(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = Lookup.get_machine_type_by_provider_id(
            json_data.get('cloud_provider_id'),
            json_data.get('limit'),
            json_data.get('page_number')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_machine_type_by_provider_id_and_machine_type_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = Lookup.get_machine_type_by_provider_id_and_machine_type_id(
            json_data.get('cloud_provider_id')[0], json_data.get("machine_type_id")[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_disk_machine_types(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_disk_machine_type()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_credential_types(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_credential_type()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_engine_cluster_instance_status(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_engine_cluster_instance_status()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_compute_type(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_spark_compute_type()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_infra_version(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_spark_infra_version()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_job_status(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_spark_job_status()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_workflow_execution_state(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_workflow_execution_state()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_workflow_type(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_workflow_type()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Volume Configuration
def create_volume(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = VolumeConfiguration.add_volume_config(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_volume(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = VolumeConfiguration.list_volume_config(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_volume(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = VolumeConfiguration.search_volume_config(
            json_data.get('volume_conf_name'),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_volume(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = VolumeConfiguration.get_volume_config_by_id_or_name(
            json_data.get('volume_conf_id'),
            json_data.get('volume_conf_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_volume(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        json_data = change_output(remove_output(args))

        if json_data.get('volume_conf_id') is not None:
            del json_data['volume_conf_id']
        if json_data.get('volume_conf_name') is not None:
            del json_data['volume_conf_name']

        response_json, status_code = VolumeConfiguration.edit_volume_config_by_id_or_name(
            json_data,
            trim_json_data.get('volume_conf_id'),
            trim_json_data.get('volume_conf_name'))
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_volume(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = VolumeConfiguration.delete_volume_config_by_id_or_name(
            json_data.get('volume_conf_id'),
            json_data.get('volume_conf_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Network Configuration
def create_network(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = NetworkConfiguration.add_network_config_by_cp_id(
            json_data
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_network(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NetworkConfiguration.list_network_config_by_cp_id(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider'))

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_network(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NetworkConfiguration.search_network_config_by_cp_id(
            json_data.get("network_conf_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider'))

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_network(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NetworkConfiguration.get_network_config_by_id_or_name(
            json_data.get('network_conf_id'),
            json_data.get('network_conf_name'))
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_network(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('network_conf_id') is not None:
            del json_data['network_conf_id']
        if json_data.get('network_conf_name') is not None:
            del json_data['network_conf_name']

        response_json, status_code = NetworkConfiguration.edit_network_config_by_id_or_name(
            json_data,
            trim_json_data.get('network_conf_id'),
            trim_json_data.get('network_conf_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_network(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = NetworkConfiguration.delete_network_config_by_id_or_name(
            json_data.get('network_conf_id'),
            json_data.get('network_conf_name'))
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Boot Disk Image Configuration
def create_boot_disk_image_config(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = BootDiskImageConfiguration.add_boot_disk_image_config(
            json_data
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_boot_disk_image_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = BootDiskImageConfiguration.list_boot_disk_image_config(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider')
        )

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_boot_disk_image_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = BootDiskImageConfiguration.search_boot_disk_image_config(
            json_data.get("boot_disk_image_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider')
        )

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_boot_disk_image_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = BootDiskImageConfiguration.get_boot_disk_image_config(
            json_data.get('boot_disk_image_id'),
            json_data.get('boot_disk_image_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_boot_disk_image_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('boot_disk_image_id') is not None:
            del json_data['boot_disk_image_id']
        if json_data.get('boot_disk_image_name') is not None:
            del json_data['boot_disk_image_name']

        response_json, status_code = BootDiskImageConfiguration.edit_boot_disk_image_config(
            json_data,
            trim_json_data.get('boot_disk_image_id'),
            trim_json_data.get('boot_disk_image_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_boot_disk_image_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = BootDiskImageConfiguration.delete_boot_disk_image_config(
            json_data.get('boot_disk_image_id'),
            json_data.get('boot_disk_image_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Credentials Configuration
def create_credential(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = CredentialsConfig.add_credentials_config(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_credentials(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = CredentialsConfig.list_credentials_config(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_credentials(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = CredentialsConfig.search_credentials_config(
            json_data.get("credentials_conf_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_credential(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = CredentialsConfig.get_credentials_config_by_id_or_name(
            json_data.get('credentials_conf_id'),
            json_data.get('credentials_conf_name'),
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_credential(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = CredentialsConfig.edit_credentials_config_by_id_or_name(
            json_data,
            json_data.get('credentials_conf_id'),
            json_data.get('credentials_conf_name')
        )
        confirm_output(response_json, status_code, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_credential(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = CredentialsConfig.delete_credentials_config_by_id_or_name(
            json_data.get('credentials_conf_id'),
            json_data.get('credentials_conf_name'),
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Cloud Environment
def create_cloud_env(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = CloudEnvironment.add_cloud_env(
            json_data
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_cloud_envs(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = CloudEnvironment.list_cloud_env(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider')
        )

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_cloud_envs(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = CloudEnvironment.search_cloud_env(
            json_data.get("cloud_env_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider')
        )

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_cloud_env(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = CloudEnvironment.get_cloud_env(
            json_data.get('cloud_env_id'),
            json_data.get('cloud_env_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_cloud_env(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('cloud_env_id') is not None:
            del json_data['cloud_env_id']
        if json_data.get('cloud_env_name') is not None:
            del json_data['cloud_env_name']

        response_json, status_code = CloudEnvironment.edit_cloud_env(
            json_data,
            trim_json_data.get('cloud_env_id'),
            trim_json_data.get('cloud_env_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_cloud_env(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = CloudEnvironment.delete_cloud_env(
            json_data.get('cloud_env_id'),
            json_data.get('cloud_env_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Object Storage Manager Configuration
def create_object_storage_manager(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = ObjectStorageManager.add_object_storage_manager(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_object_storage_manager(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManager.list_object_storage_manager(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_object_storage_manager(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManager.search_object_storage_manager(
            json_data.get("object_storage_manager_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_object_storage_manager(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManager.get_object_storage_manager_by_id_or_name(
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_object_storage_manager(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('object_storage_manager_id') is not None:
            del json_data['object_storage_manager_id']
        if json_data.get('object_storage_manager_name') is not None:
            del json_data['object_storage_manager_name']

        response_json, status_code = ObjectStorageManager.edit_object_storage_manager_by_id_or_name(
            json_data,
            trim_json_data.get('object_storage_manager_id'),
            trim_json_data.get('object_storage_manager_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_object_storage_manager(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManager.delete_object_storage_manager_by_id_or_name(
            trim_json_data.get('object_storage_manager_id'),
            trim_json_data.get('object_storage_manager_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Object Storage Manager Files Configuration
def create_object_storage_manager_files(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        if (trim_json_data.get('local_file_path') != None and os.path.isfile(trim_json_data.get('local_file_path'))):

            response_json, status_code = ObjectStorageManagerFiles.add_object_storage_manager_files(
                trim_json_data.get('local_file_path'),
                trim_json_data.get('overwrite'),
                trim_json_data.get('object_storage_manager_id'),
                trim_json_data.get('object_storage_manager_name'),
                trim_json_data.get('cluster_id'),
                trim_json_data.get('cluster_name')
            )
            confirm_output(response_json, status_code, trim_json_data)

        elif (trim_json_data.get('local_file_path') == None):
            logger.error("Please provide a local file path\n")
            sys.exit(-1)

        else:
            file_error = {
                "error": f"The file cannot be found at '{trim_json_data.get('local_file_path')}'"}
            logger.error(json.dumps(file_error, indent=2))
            sys.exit(-1)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManagerFiles.get_object_storage_manager_files_by_id_or_name(
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name'),
            json_data.get('file_id'),
            json_data.get('file_name')
        )

        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManagerFiles.list_object_storage_manager_files_by_id_or_name(
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManagerFiles.search_object_storage_manager_files_by_id_or_name_and_file_name(
            json_data.get('file_name'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManagerFiles.delete_object_storage_manager_file_by_id_or_name(
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name'),
            json_data.get('file_id'),
            json_data.get('file_name')
        )
        confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Hive Metastore Configuration
def create_hive_metastore_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        json_data = createOrUpdateHiveMetastoreConfig(
            change_output(remove_output(args)))

        json_data["name"] = trim_json_data.get('name')

        response_json, status_code = HiveMetastoreConfiguration.add_hive_metastore_configuration(
            json_data)

        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_hive_metastore_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = HiveMetastoreConfiguration.list_hive_metastore_config(
            json_data.get('page_number'),
            json_data.get('limit'))
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_hive_metastore_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = HiveMetastoreConfiguration.search_hive_metastore_config(
            json_data.get('hive_metastore_conf_name'),
            json_data.get('page_number'),
            json_data.get('limit'))
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_hive_metastore_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = HiveMetastoreConfiguration.get_hive_metastore_config_by_id_or_name(
            json_data.get('hive_metastore_conf_id'),
            json_data.get('hive_metastore_conf_name'))
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_hive_metastore_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        json_data = createOrUpdateHiveMetastoreConfig(
            change_output(remove_output(args)))

        if hasattr(args, 'name') and trim_json_data.get('name') != None:
            json_data["name"] = trim_json_data.get('name')

        response_json, status_code = HiveMetastoreConfiguration.edit_hive_metastore_config(
            json_data,
            trim_json_data.get('hive_metastore_conf_id'),
            trim_json_data.get('hive_metastore_conf_name'))

        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_hive_metastore_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = HiveMetastoreConfiguration.delete_hive_metastore_config_by_id(
            trim_json_data.get('hive_metastore_conf_id'),
            trim_json_data.get('hive_metastore_conf_name'))

        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
