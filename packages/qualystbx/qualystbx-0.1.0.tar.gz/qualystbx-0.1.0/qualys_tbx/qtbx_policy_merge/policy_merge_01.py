from qualys_tbx import qtbx_lib
import base64
import argparse
import requests
import json
import sys
from pathlib import Path
import re
import time
import os
import copy
import xmltodict
from lxml import etree
from lxml.etree import CDATA
from qualys_tbx.qtbx_lib import qtbx_lib_authentication
from qualys_tbx.qtbx_lib import qtbx_lib_functions
from qualys_tbx.qtbx_lib import qtbx_lib_config
from qualys_tbx.qtbx_lib import qtbx_lib_argparser
from qualys_tbx.qtbx_lib import qtbx_lib_logger
import qualys_tbx


def usage():
    usage_text = '''\
    Usage: To execute policy_merge, set the required environment variables and then run the script as follows:

    Set Environment Variables on Linux or macOS:
        export q_username="your_q_username_here"
        export q_password="your_q_password_here"
        export q_api_fqdn_server="your qualys platform fqdn, e.g., qualysapi.qualys.com"

    Set Environment Variables on Windows (Command Prompt):
        set q_username="your_q_username_here"
        set q_password="your_q_password_here"
        set q_api_fqdn_server="your qualys platform fqdn, e.g., qualysapi.qualys.com"

    Note: In Windows PowerShell, use $env: instead of set, like this:
        $env:q_username="your_q_username_here"
        $env:q_password="your_q_password_here"
        $env:q_api_fqdn_server="your qualys platform fqdn, e.g., qualysapi.qualys.com"

    Run Command:
        python qualystbx.py --execute policy_merge --new_policy_id=[new_policy_id] --old_policy_id=[old_policy_id] --cid_list=[optional, comma-separated list of cids to move from old policy to new policy, all if excluded] [optional --log_to_console will log to console instead of file]

    Options:
        --new_policy_id=9001     - The new policy id you would like to merge old cids into.
        --old_policy_id=9000     - The old policy id with cids you customized.
        --cid_list=2020,222,444  - (optional) Comma-separated list of cids to move from old policy to new policy.

    Ensure all required environment variables are set before running the script.
    '''
    print(usage_text)


def read_xml_into_dict(xml_file) -> dict:
    xml_dict = {}
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
            xml_dict = xmltodict.parse(file_content)  # Parse and store as dict
            qtbx_lib_logger.logger.info(f"XML file has been read into dict: {xml_file}")
    except Exception as e:
        qtbx_lib_logger.logger.error(f"Error reading the XML file: {e}")

    return xml_dict


def traverse_xml_encapsulating_in_cdata_where_special_chars_exists(xml_string):
    xml_bytes = xml_string.encode('utf-8')
    xml_parser = etree.XMLParser(encoding='utf-8')
    xml_root = etree.fromstring(xml_bytes, parser=xml_parser)

    def do_special_chars_exist_requiring_cdata(text):
        special_chars = ["<", ">", "&"]
        return any(char in text for char in special_chars)

    def traverse_xml_tree_and_encapsulate_with_cdata_when_special_chars_exists(node):
        if node.text and do_special_chars_exist_requiring_cdata(node.text):
            node.text = CDATA(node.text)
        for child in node:
            traverse_xml_tree_and_encapsulate_with_cdata_when_special_chars_exists(child)

    traverse_xml_tree_and_encapsulate_with_cdata_when_special_chars_exists(xml_root)
    xml_bytes = etree.tostring(xml_root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    xml_output_string = xml_bytes.decode('utf-8')
    return xml_output_string



def get_control_list_from_policy(q_dict, controls_list):
    q_dict_updated = q_dict.copy()
    for data_key in q_dict_updated:
        try:
            # Attempt to navigate through nested dictionaries
            sections = q_dict_updated[data_key]['RESPONSE']['POLICY']['SECTIONS']['SECTION']
            for section in sections:
                try:
                    # Filter controls based on 'ID' being in the provided controls_list
                    filtered_controls = [control for control in section['CONTROLS']['CONTROL']
                                         if control['ID'] in controls_list]
                    # Update the section with filtered controls and the total count
                    section['CONTROLS']['CONTROL'] = filtered_controls
                    section['CONTROLS']['@total'] = str(len(filtered_controls))
                except KeyError:
                    # Handle missing keys within the section or controls
                    qtbx_lib_logger.logger_error(f"Key error in section controls for data key {data_key}, possibly missing 'CONTROL' or 'ID'.")
        except KeyError:
            # Handle missing keys in the path to sections
            qtbx_lib_logger.logger_error(f"Key error in retrieving sections for data key {data_key}, check 'RESPONSE', 'POLICY', 'SECTIONS', or 'SECTION'.")

    return q_dict_updated


def export_policy(output_file_path, policy_id, api_fqdn_server, username, headers):
    payload = {}
    # action=export&id=2645453&show_user_controls=1&show_appendix=1
    url = f"https://{api_fqdn_server}/api/2.0/fo/compliance/policy/?action=export&id={policy_id}&show_user_controls=1"
    qtbx_lib_logger.logger_info(f"Executing export_policy: {url} ")

    qtbx_lib_authentication.extract_qualys(
        try_extract_max_count=3,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=300,
        chunk_size_calc=10240,
        output_file=output_file_path,
        q_username=username,
        requests_module_tls_verify_status=True,
        compression_method=open,
        request_method="POST"
    )


def import_policy(results_file_path, payload_policy_to_import, api_fqdn_server, username, headers, title):
    url = f"https://{api_fqdn_server}/api/2.0/fo/compliance/policy/?action=import&title={title}&create_user_controls=1"
    qtbx_lib_logger.logger_info(f"Executing import_policy: {url} ")

    qtbx_lib_authentication.extract_qualys(
        try_extract_max_count=3,
        url=url,
        headers=headers,
        payload=payload_policy_to_import,
        http_conn_timeout=300,
        chunk_size_calc=10240,
        output_file=results_file_path,
        q_username=username,
        requests_module_tls_verify_status=True,
        compression_method=open,
        request_method="POST"
    )


def merge_policy(results_file_path, payload_policy_to_merge, policy_id, api_fqdn_server, username, headers):
    url = f"https://{api_fqdn_server}/api/2.0/fo/compliance/policy/?action=merge&id={policy_id}&update_existing_controls=1"
    qtbx_lib_logger.logger_info(f"Executing merge_policy: {url} ")

    qtbx_lib_authentication.extract_qualys(
        try_extract_max_count=3,
        url=url,
        headers=headers,
        payload=payload_policy_to_merge,
        http_conn_timeout=300,
        chunk_size_calc=10240,
        output_file=results_file_path,
        q_username=username,
        requests_module_tls_verify_status=True,
        compression_method=open,
        request_method="POST"
    )


def write_dict_to_xml(data, file_path):
    try:
        xml_string = xmltodict.unparse(data, pretty=True)
        with open(file_path, 'w') as xml_file:
            xml_file.write(xml_string)
        qtbx_lib_logger.logger_info(f"XML file written:{file_path}")

    except Exception as e:
        qtbx_lib_logger.logger_error(f"XML file not writtern, An error occurred: {e}")
        qtbx_lib_logger.logger_error(f"XML file name: {file_path}")
        sys.exit(1)


def main(qualystbx=""):
    # Get Arguments, cid list to merge and qualys auth
    policy_arguments = qtbx_lib_argparser.GetPolicyMergeArgs(logger=qtbx_lib_logger.logger)
    cid_list = [str(cid) for cid in policy_arguments.args.cid_list]
    qtbx_credentials_dict = qtbx_lib_authentication.get_credentials_from_env()

    # Old policy results
    old_policy_id = policy_arguments.args.old_policy_id
    old_policy_output_file_path = Path(qtbx_lib_config.qtbx_data_dir, "old_policy_id.xml")
    old_policy_cid_list_output_file_path = Path(qtbx_lib_config.qtbx_data_dir, "old_policy_id_cid_list_for_merge.xml")

    # New policy results
    new_policy_id = policy_arguments.args.new_policy_id
    new_policy_output_file_path = Path(qtbx_lib_config.qtbx_data_dir, "new_policy_id.xml")
    import_new_policy_results_file_path = Path(qtbx_lib_config.qtbx_data_dir, "import_new_policy_results_file.xml")

    # Results of merge
    merged_policy_results_file_path = Path(qtbx_lib_config.qtbx_data_dir, "merged_policy_results_file.xml")
    merged_policy_output_file_path = Path(qtbx_lib_config.qtbx_data_dir, "merged_policy_id_file.xml")

    # Export the old policy
    export_policy(
        output_file_path=old_policy_output_file_path,
        policy_id=old_policy_id,
        api_fqdn_server=qtbx_credentials_dict['q_api_fqdn_server'],
        username=qtbx_credentials_dict['q_username'],
        headers=qtbx_credentials_dict['headers']
    )

    # Export the new policy
    export_policy(
        output_file_path=new_policy_output_file_path,
        policy_id=new_policy_id,
        api_fqdn_server=qtbx_credentials_dict['q_api_fqdn_server'],
        username=qtbx_credentials_dict['q_username'],
        headers=qtbx_credentials_dict['headers']
    )

    # Read policies into dictionary
    old_policy_dict = read_xml_into_dict(old_policy_output_file_path)
    new_policy_dict = read_xml_into_dict(new_policy_output_file_path)

    # Prepare new policy title for merge
    new_policy_xml = xmltodict.unparse(new_policy_dict, pretty=True)
    new_policy_title = f"MERGED_POLICY_{qtbx_lib_functions.get_utc_datetime()}_{new_policy_dict['POLICY_EXPORT_OUTPUT']['RESPONSE']['POLICY']['TITLE']}"
    qtbx_lib_logger.logger_info(f"Policies exported - old_policy_id: {old_policy_id}, new_policy_id: {new_policy_id}")

    # Get Policy with only CID List included and write to disk.
    policy_dict_updated = get_control_list_from_policy(old_policy_dict,cid_list)
    write_dict_to_xml(data=policy_dict_updated, file_path=old_policy_cid_list_output_file_path)

    # Begin merging policy by first creating a new policy to merge into.
    qtbx_lib_logger.logger_info(f"Begin creating new merged policy: {new_policy_title}")
    headers_for_import = copy.deepcopy(qtbx_credentials_dict['headers'])
    headers_for_import['Content-Type'] = 'text/xml'
    import_policy(
        results_file_path=import_new_policy_results_file_path,
        payload_policy_to_import=new_policy_xml,
        api_fqdn_server=qtbx_credentials_dict['q_api_fqdn_server'],
        username=qtbx_credentials_dict['q_username'],
        headers=headers_for_import,
        title=new_policy_title
    )

    # Merge CID List into new policy.
    merge_policy_information_dict = read_xml_into_dict(import_new_policy_results_file_path)
    merge_policy_id = merge_policy_information_dict['SIMPLE_RETURN']['RESPONSE']['ITEM_LIST']['ITEM'][0]['VALUE']
    merge_policy_xml = xmltodict.unparse(policy_dict_updated, pretty=True)
    headers_for_merge = copy.deepcopy(headers_for_import)
    merge_policy(
        policy_id=merge_policy_id,
        results_file_path=merged_policy_results_file_path,
        payload_policy_to_merge=merge_policy_xml,
        api_fqdn_server=qtbx_credentials_dict['q_api_fqdn_server'],
        username=qtbx_credentials_dict['q_username'],
        headers=headers_for_merge
    )

    # Export results of Policy Merged.
    export_policy(
        output_file_path=merged_policy_output_file_path,
        policy_id=merge_policy_id,
        api_fqdn_server=qtbx_credentials_dict['q_api_fqdn_server'],
        username=qtbx_credentials_dict['q_username'],
        headers=qtbx_credentials_dict['headers']
    )

    qtbx_lib_logger.logger_info(f"End creating new merged policy: {new_policy_title}")



if __name__ == "__main__":
    policy_arguments = qtbx_lib_argparser.GetPolicyMergeArgs()


# def parse_args():
#     parser = argparse.ArgumentParser(description="Merge cids from an old policy to a new policy.")
#     parser.add_argument("--execute", type=str, required=True,
#                         help="The Qualys ToolBox component you wish to execute.")
#     parser.add_argument("--storage_dir", type=str, required=True,
#                         help="The storage directory where all data will be stored.")
#     parser.add_argument("--new_policy_id", type=int, required=True,
#                         help="The new policy id you would like to merge old cids into.")
#     parser.add_argument("--old_policy_id", type=int, required=True, help="The old policy id with cids you customized.")
#     parser.add_argument("--cid_list", type=str,
#                         help="(optional) Comma separated list of cids to move from old policy to new policy.",
#                         default="")
#     args = parser.parse_args()
#     return args


# def print_arguments(args):
#     print("Arguments entered:")
#     print(f"New Policy ID: {args.new_policy_id}")
#     print(f"Old Policy ID: {args.old_policy_id}")
#     if args.cid_list:
#         print(f"CID List: {args.cid_list}")
#     else:
#         print("CID List: None (All CIDs from the old policy will be considered)")


# def get_args():
#     args = parse_args()
#     print_arguments(args)
#     cid_list = [int(cid) for cid in args.cid_list.split(",")] if args.cid_list else []
#     print(f"\nMerging CIDs from old policy {args.old_policy_id} to new policy {args.new_policy_id}.")
#     if cid_list:
#         print(f"Specific CIDs to move: {cid_list}")
#     else:
#         print("Moving all CIDs from the old policy to the new policy.")
#     return args

# def populate_q_dict_from_stdin():
#     if sys.stdin.isatty():
#         # No data provided via stdin, print usage message and exit
#         usage()
#         sys.exit(1)
#
#     # Read JSON string from stdin
#     input_json = sys.stdin.read().strip()
#
#     # Exit if the input is empty
#     if not input_json:
#         print("Error: No input provided. Please provide a JSON string via stdin.")
#         usage()
#         sys.exit(1)
#
#     # Decode the JSON string into a Python dictionary
#     q_dict = json.loads(input_json)
#     return q_dict


# def prepare_export_policy_id_api_call() -> dict:
#     # VARIABLES
#     q_dict = populate_q_dict_from_stdin()
#     required_keys = ["q_username", "q_password", "q_api_fqdn_server", "q_policy_id_to_export"]
#     missing_keys = [key for key in required_keys if key not in q_dict]
#     if missing_keys:
#         print("Error: The following required keys are missing from the input JSON: " + ", ".join(missing_keys))
#         print("Please ensure all keys are present and try again.")
#         usage()
#         sys.exit(1)
#     q_dict['q_base64_credentials'] = qtbx_lib_qapi.encode_credentials(q_dict['q_username'], q_dict['q_password'])
#     q_dict['headers'] = {
#         'X-Requested-With': f'{qualys_tbx.__version__}',
#         'Authorization': f"Basic {q_dict['q_base64_credentials']}"
#     }
#     return q_dict

# def prepare_export_policy_id_api_call() -> dict:
#     # Required keys that should be set in environment variables
#     required_keys = ["q_username", "q_password", "q_api_fqdn_server"]
#     q_dict = {}
#
#     # Check for missing required environment variables
#     missing_keys = [key for key in required_keys if key not in os.environ]
#     if missing_keys:
#         print("Error: The following required environment variables are missing: " + ", ".join(missing_keys))
#         print("Please ensure all keys are present in your environment and try again.")
#         usage()  # Assuming there's a function usage() that describes how to set environment variables
#         sys.exit(1)
#
#     # Populate q_dict with values from environment variables
#     for key in required_keys:
#         q_dict[key] = os.environ[key]
#
#     # Encode credentials
#     q_dict['q_base64_credentials'] = qtbx_lib_qapi.encode_credentials(q_dict['q_username'], q_dict['q_password'])
#
#     # Set headers
#     q_dict['headers'] = {
#         'X-Requested-With': f'{qualys_tbx.__version__}',
#         'Authorization': f"Basic {q_dict['q_base64_credentials']}"
#     }
#
#     return q_dict



# def get_credentials_from_stdin() -> dict:
#     # VARIABLES
#     q_dict = populate_q_dict_from_stdin()
#     required_keys = ["q_username", "q_password", "q_api_fqdn_server"]
#     missing_keys = [key for key in required_keys if key not in q_dict]
#     if missing_keys:
#         print("Error: The following required keys are missing from the input JSON: " + ", ".join(missing_keys))
#         print("Please ensure all keys are present and try again.")
#         usage()
#         sys.exit(1)
#     q_dict['q_base64_credentials'] = qtbx_lib_qapi.encode_credentials(q_dict['q_username'], q_dict['q_password'])
#     q_dict['headers'] = {
#         'X-Requested-With': f'{qualys_tbx.__version__}',
#         'Authorization': f"Basic {q_dict['q_base64_credentials']}"
#     }
#     return q_dict


# def prepare_merge_policy_between_ids_in_qualys_api_call() -> dict:
#     q_dict = populate_q_dict_from_stdin()
#     required_keys = ["q_username", "q_password", "q_api_fqdn_server", "q_policy_id_update_existing_controls",
#                      "q_old_policy_id"]
#     missing_keys = [key for key in required_keys if key not in q_dict]
#     if missing_keys:
#         print("Error: The following required keys are missing from the input JSON: " + ", ".join(missing_keys))
#         print("Please ensure all keys are present and try again.")
#         usage()
#         sys.exit(1)
#     q_dict['q_base64_credentials'] = qtbx_lib_qapi.encode_credentials(q_dict['q_username'], q_dict['q_password'])
#     q_dict['headers'] = {
#         'X-Requested-With': f'{qualys_tbx.__version__}',
#         'Authorization': f"Basic {q_dict['q_base64_credentials']}"
#     }
#     return q_dict


# def prepare_merge_policy_from_file_to_id_in_qualys_api_call() -> dict:
#     # VARIABLES
#     q_dict = populate_q_dict_from_stdin()
#     required_keys = ["q_username", "q_password", "q_api_fqdn_server", "q_policy_id_update_existing_controls"]
#     missing_keys = [key for key in required_keys if key not in q_dict]
#     if missing_keys:
#         print("Error: The following required keys are missing from the input JSON: " + ", ".join(missing_keys))
#         print("Please ensure all keys are present and try again.")
#         usage()
#         sys.exit(1)
#     q_dict['q_base64_credentials'] = qtbx_lib_qapi.encode_credentials(q_dict['q_username'], q_dict['q_password'])
#     q_dict['headers'] = {
#         'X-Requested-With': f'{qualys_tbx.__version__}',
#         'Authorization': f"Basic {q_dict['q_base64_credentials']}"
#     }
#     return q_dict
#
#
# def merge_policies_within_qualys():
#     # VARIABLES
#     q_dict: dict = prepare_merge_policy_between_ids_in_qualys_api_call()
#     output_file = f"data/merge_policy_id_{q_dict['q_policy_id_update_existing_controls']}_merge_policy_id_{q_dict['q_old_policy_id']}_results_file.xml"
#     payload = {}
#     url = f"https://{q_dict['q_api_fqdn_server']}/api/2.0/fo/compliance/policy/?action=merge&id={q_dict['q_policy_id_update_existing_controls']}&merge_policy_id={q_dict['q_old_policy_id']}&update_existing_controls=1"
#     if q_dict['q_preview_merge'].__contains__("1"):
#         url = url + "&preview_merge=1"
#
#     print(f"Executing merge_policies: {url} ")
#     response = qtbx_lib_qapi.extract_qualys(
#         try_extract_max_count=3,
#         url=url,
#         headers=q_dict['headers'],
#         payload=payload,
#         http_conn_timeout=300,
#         chunk_size_calc=10240,
#         output_file=output_file,
#         q_username=q_dict['q_username'],
#         requests_module_tls_verify_status=True,
#         compression_method=open,
#         request_method="POST"
#     )
#     print(f"merge results are: {output_file}")


# def merge_policies_from_file():
#     # VARIABLES
#     q_dict: dict = prepare_merge_policy_between_ids_in_qualys_api_call()
#     output_file = f"data/merge_policy_id_{q_dict['q_policy_id_update_existing_controls']}_merge_policy_id_{q_dict['q_old_policy_id']}_results_file.xml"
#     payload = {}
#     url = f"https://{q_dict['q_api_fqdn_server']}/api/2.0/fo/compliance/policy/?action=merge&id={q_dict['q_policy_id_update_existing_controls']}&merge_policy_id={q_dict['q_old_policy_id']}&update_existing_controls=1"
#     if q_dict['q_preview_merge'].__contains__("1"):
#         url = url + "&preview_merge=1"
#
#     print(f"Executing merge_policies: {url} ")
#     response = qtbx_lib_qapi.extract_qualys(
#         try_extract_max_count=3,
#         url=url,
#         headers=q_dict['headers'],
#         payload=payload,
#         http_conn_timeout=300,
#         chunk_size_calc=10240,
#         output_file=output_file,
#         q_username=q_dict['q_username'],
#         requests_module_tls_verify_status=True,
#         compression_method=open,
#         request_method="POST"
#     )
#     print(f"merge results are: {output_file}")


# def get_policy_list(q_username, q_password, q_api_fqdn):
#     # VARIABLES
#     q_dict: dict = prepare_merge_policy_between_ids_in_qualys_api_call()
#     output_file = f"data/merge_policy_id_{q_dict['q_policy_id_update_existing_controls']}_merge_policy_id_{q_dict['q_old_policy_id']}_results_file.xml"
#     payload = {}
#     url = f"https://{q_dict['q_api_fqdn_server']}/api/2.0/fo/compliance/policy/?action=merge&id={q_dict['q_policy_id_update_existing_controls']}&merge_policy_id={q_dict['q_old_policy_id']}&update_existing_controls=1"
#     if q_dict['q_preview_merge'].__contains__("1"):
#         url = url + "&preview_merge=1"
#
#     print(f"Executing merge_policies: {url} ")
#     response = qtbx_lib_qapi.extract_qualys(
#         try_extract_max_count=3,
#         url=url,
#         headers=q_dict['headers'],
#         payload=payload,
#         http_conn_timeout=300,
#         chunk_size_calc=10240,
#         output_file=output_file,
#         q_username=q_dict['q_username'],
#         requests_module_tls_verify_status=True,
#         compression_method=open,
#         request_method="POST"
#     )
#     print(f"merge results are: {output_file}")



# def write_json(q_dict, data_dict):
#     for q_policy_id in q_dict['q_policy_id_to_export']:
#         try:
#             output_file = f"data/export_policy_id_{q_policy_id}_updated_file.json"
#             with open(output_file, 'w', encoding='utf-8') as file:
#                 xml_policy_dict = data_dict[q_policy_id]
#                 json.dump(xml_policy_dict, file)
#             print(f"JSON file has been written to {output_file}")
#         except Exception as e:
#             print(f"Error writing the JSON file: {e}")
#
#
# def write_xml(q_dict, data_dict):
#     for q_policy_id in q_dict['q_policy_id_to_export']:
#         try:
#             output_file = f"data/export_policy_id_{q_policy_id}_updated_file.xml"
#             with open(output_file, 'w', encoding='utf-8') as file:
#                 xml_policy_dict = data_dict[q_policy_id]
#                 xml_str = xmltodict.unparse(xml_policy_dict, pretty=True, encoding='utf-8', short_empty_elements=False)
#                 xml_str_cdata = traverse_xml_encapsulating_in_cdata_where_special_chars_exists(xml_str)
#                 file.write(xml_str_cdata)
#             print(f"XML file has been written to {output_file}")
#         except Exception as e:
#             print(f"Error writing the XML file: {e}")

#
# def modify_policy_dict(poicy_dict, keep_cids_list):
#     pass
#

# def get_control_list_from_policy(q_dict, controls_list):
#     q_dict_updated = q_dict.copy()
#     for data_key in q_dict_updated:
#         for section in q_dict_updated[data_key]['RESPONSE']['POLICY']['SECTIONS']['SECTION']:
#             filtered_controls = [control for control in section['CONTROLS']['CONTROL']
#                                  if control['ID'] in controls_list]
#             section['CONTROLS']['CONTROL'] = filtered_controls
#             section['CONTROLS']['@total'] = str(len(filtered_controls))
#     return q_dict_updated