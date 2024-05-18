import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
from urllib.parse import urlencode, quote_plus

import requests
import time
import base64
from pathlib import Path
import re
import os
import sys
import qualys_tbx
from qualys_tbx.qtbx_lib import qtbx_lib_logger
global qtbx_credentials_dict

code_version = "policy_compliance_merge_v1.0"
http_error_codes_v2_api = {
    "202": "Retry Later Duplicate Operation.",
    "400": "Bad Request Unrecognized parameter",
    "401": "Unauthorized check credentials.",
    "403": "Forbidden User account is inactive or user license not authorized for API. ",
    "409": "Conflict Check Concurrency and Rate Limits.",
    "501": "Internal Error.",
    "502": "Gateway Error",
    "503": "Maintenance we are performing scheduled maintenance on our system.",
    "504": "Gateway Error.",
}


def get_requests_module_tls_verify_status_from_env():
    if 'q_tls_verify_status' in os.environ:
        if os.environ['q_tls_verify_status'] in {'False', 'false', 'f', 'n', 'no'}:
            qtbx_lib_logger.logger_warning(
                "q_tls_verify_status is False.  This is not a recommended setting as you could be "
                "subject to man in the middle attack.")
            return False

    qtbx_lib_logger.logger_info("q_tls_verify_status is True.  This is default recommended setting.")
    return True


def get_credentials_from_env() -> dict:
    required_keys = ["q_username", "q_password", "q_api_fqdn_server"]
    q_dict = {}

    def usage():
        pass

    # Check for missing required environment variables
    missing_keys = [key for key in required_keys if key not in os.environ]
    if missing_keys:
        qtbx_lib_logger.logger_error("Error: The following required environment variables are missing: " + ", ".join(missing_keys))
        qtbx_lib_logger.logger_error("Please ensure all keys are present in your environment and try again.")
        usage()  # Assuming there's a function usage() that describes how to set environment variables
        sys.exit(1)

    # Populate q_dict with values from environment variables
    for key in required_keys:
        q_dict[key] = os.environ[key]

    # Encode credentials
    q_dict['q_base64_credentials'] = get_base64_encoding(username=q_dict['q_username'], password=q_dict['q_password'])

    # Set headers
    q_dict['headers'] = {
        'X-Requested-With': f'{qualys_tbx.__version__}',
        'Authorization': f"Basic {q_dict['q_base64_credentials']}"
    }
    q_dict['q_gateway_fqdn_server'] = get_gateway_platform_fqdn(q_dict['q_api_fqdn_server'])
    q_dict['bearer'] = get_bearer_token(q_dict['q_username'], q_dict['q_password'], q_dict['q_api_fqdn_server'])

    return q_dict


def get_http_error_code_message_v2_api(http_error=""):
    global http_error_codes_v2_api

    if http_error in http_error_codes_v2_api.keys():
        return http_error_codes_v2_api[http_error]
    else:
        return None


def get_platform_identifier_dict(): # Update here whenever platform identification changes.
    platform_identifier_dict = {}
    platform_identifier_dict['_'] = {'qualysapi': 'qualysapi.qualys.com', 'gateway':'gateway.qg1.apps.qualys.com', 'pod': 'US_01'}
    platform_identifier_dict['2'] = {'qualysapi': 'qualysapi.qg2.apps.qualys.com','gateway': 'gateway.qg2.apps.qualys.com', 'pod': 'US_02'}
    platform_identifier_dict['3'] = {'qualysapi': 'qualysapi.qg3.apps.qualys.com','gateway': 'gateway.qg3.apps.qualys.com', 'pod': 'US_03'}
    platform_identifier_dict['6'] = {'qualysapi': 'qualysapi.qg4.apps.qualys.com','gateway': 'gateway.qg4.apps.qualys.com', 'pod': 'US_04'}
    platform_identifier_dict['-'] = {'qualysapi': 'qualysapi.qualys.eu','gateway': 'gateway.qg1.apps.qualys.eu', 'pod': 'EU_01'}
    platform_identifier_dict['5'] = {'qualysapi': 'qualysapi.qg2.apps.qualys.eu','gateway': 'gateway.qg2.apps.qualys.eu', 'pod': 'EU_02'}
    platform_identifier_dict['!'] = {'qualysapi': 'qualysapi.qg2.apps.qualys.eu','gateway': 'gateway.qg2.apps.qualys.eu', 'pod': 'EU_02'}
    platform_identifier_dict['B'] = {'qualysapi': 'qualysapi.qg3.apps.qualys.it','gateway': 'gateway.qg3.apps.qualys.it', 'pod': 'EU_03'}
    platform_identifier_dict['8'] = {'qualysapi': 'qualysapi.qg1.apps.qualys.in','gateway': 'gateway.qg1.apps.qualys.in', 'pod': 'IN_01'}
    platform_identifier_dict['9'] = {'qualysapi': 'qualysapi.qg1.apps.qualys.ca','gateway': 'gateway.qg1.apps.qualys.ca', 'pod': 'CA_01'}
    platform_identifier_dict['7'] = {'qualysapi': 'qualysapi.qg1.apps.qualys.ae','gateway': 'gateway.qg1.apps.qualys.eu', 'pod': 'AE_01'}
    platform_identifier_dict['1'] = {'qualysapi': 'qualysapi.qg1.apps.qualys.co.uk','gateway': 'gateway.qg1.apps.qualys.co.uk', 'pod': 'UK_01'}
    platform_identifier_dict['4'] = {'qualysapi': 'qualysapi.qg1.apps.qualys.com.au','gateway': 'gateway.qg1.apps.qualys.com.au', 'pod': 'AU_01'}
    platform_identifier_dict['A'] = {'qualysapi': 'qualysapi.qg1.apps.qualysksa.com','gateway': 'gateway.qg1.apps.qualysksa.com', 'pod': 'KSA_01'}
    return platform_identifier_dict


def get_platform_identification_with_fqdn(fqdn=""):
    qualys_fqdn = fqdn.strip()  # Remove any leading/trailing whitespace
    platform_identifier_dict = get_platform_identifier_dict()
    for key in platform_identifier_dict:
        platform_qualysapi_fqdn = platform_identifier_dict[key]['qualysapi']
        platform_gateway_fqdn = platform_identifier_dict[key]['gateway']
        if qualys_fqdn == platform_qualysapi_fqdn:
            return platform_identifier_dict[key]
        elif qualys_fqdn == platform_gateway_fqdn:
            return platform_identifier_dict[key]
    return None


def get_gateway_platform_fqdn(api_fqdn_server) -> str:
    platform_identification = \
        get_platform_identification_with_fqdn(api_fqdn_server)
    if platform_identification:
       gateway_fqdn_server = platform_identification['gateway']
    else:
        qtbx_lib_logger.logger_error(f"Invalid q_api_fqdn_server , gateway not found.  ")
        gateway_fqdn_server = None
    return gateway_fqdn_server


def get_base64_encoding(username="", password=""):
    auth_base64 = ""
    if username != "" and password != "":
        auth_base64 = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    return auth_base64

def get_bearer_token(q_username, q_password, api_fqdn_server, message=""):
    gateway_fqdn_server = get_gateway_platform_fqdn(api_fqdn_server)
    url = f"https://{gateway_fqdn_server}/auth"
    payload = {'token': 'true', 'password': q_password, 'username': q_username, 'permissions': 'true'}
    payload = urlencode(payload, quote_via=quote_plus)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': f'qualystbx_v{qualys_tbx.__version__} QTBXM: {message}',
        'User-Agent': f"qualystbx_v{qualys_tbx.__version__} QTBXM: {message}",
    }

    max_retries = 10
    sleep_time = 15
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            qtbx_lib_logger.logger_info(f"Bearer token for {q_username} retrieved from {gateway_fqdn_server}")
            return response.text
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                qtbx_lib_logger.logger_error(f"Authentication failed with status 401 Unauthorized for user {q_username} at gateway {gateway_fqdn_server}.")
                sys.exit(1)
            else:
                qtbx_lib_logger.logger_warning(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            qtbx_lib_logger.logger_warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(sleep_time)
                # Increase sleep time for the next attempt, cap it at 300 seconds
                sleep_time = min(sleep_time * 2, 300)
    else:
            qtbx_lib_logger.logger_error(f"All attempts failed. Reporting error for user {q_username} at gateway {gateway_fqdn_server}.")
            sys.exit(1)


def get_qualys_headers(request=None):
    # 'X-Powered-By': 'Qualys:USPOD1:a6df6808-8c45-eb8c-e040-10ac13041e17:9e42af6e-c5a2-4d9e-825c-449440445cc8'
    # 'X-RateLimit-Limit': '2000'
    # 'X-RateLimit-Window-Sec': '3600'
    # 'X-Concurrency-Limit-Limit': '10'
    # 'X-Concurrency-Limit-Running': '0'
    # 'X-RateLimit-ToWait-Sec': '0'
    # 'X-RateLimit-Remaining': '1999'
    # 'Keep-Alive': 'timeout=300, max=250'
    # 'Connection': 'Keep-Alive'
    # 'Transfer-Encoding': 'chunked'
    # 'Content-Type': 'application/xml'
    if request is None:
        pass
    else:
        request_url = request.url
        url_fqdn = re.sub("(https://)([0-9a-zA-Z\.\_\-]+)(/.*$)", "\g<2>", request_url)
        url_end_point = re.sub("(https://[0-9a-zA-Z\.\_\-]+)/", "", request_url)
        headers = {}
        if 'X-RateLimit-Limit' in request.headers.keys():
            x_ratelimit_limit = request.headers['X-RateLimit-Limit']
            headers['x_ratelimit_limit'] = x_ratelimit_limit

        if 'X-RateLimit-Window-Sec' in request.headers.keys():
            x_ratelimit_window_sec = request.headers['X-RateLimit-Window-Sec']
            headers['x_ratelimit_window_sec'] = x_ratelimit_window_sec

        if 'X-RateLimit-ToWait-Sec' in request.headers.keys():
            x_ratelimit_towait_sec = request.headers['X-RateLimit-ToWait-Sec']
            headers['x_ratelimit_towait-sec'] = x_ratelimit_towait_sec

        if 'X-RateLimit-Remaining' in request.headers.keys():
            x_ratelimit_remaining = request.headers['X-RateLimit-Remaining']
            headers['x_ratelimit_remaining'] = x_ratelimit_remaining

        if 'X-Concurrency-Limit-Limit' in request.headers.keys():
            x_concurrency_limit_limit = request.headers['X-Concurrency-Limit-Limit']
            headers['x_concurrency_limit_limit'] = x_concurrency_limit_limit

        if 'X-Concurrency-Limit-Running' in request.headers.keys():
            x_concurrency_limit_running = request.headers['X-Concurrency-Limit-Running']
            headers['x_concurrency_limit_running'] = x_concurrency_limit_running

        headers['url'] = request_url
        headers['api_fqdn_server'] = url_fqdn
        headers['api_end_point'] = url_end_point

        return headers



def extract_qualys(
        try_extract_max_count=30,
        url=None,
        headers=None,
        payload=None,
        http_conn_timeout=300,
        chunk_size_calc=10240,
        output_file=None,
        q_username=None,
        requests_module_tls_verify_status=True,
        compression_method=open,
        request_method="POST"
):
    time_sleep = 0
    requests_abort_error_status_codes = {202, 500, 504, 501, 520, 502}
    requests_concurrency_error_status_codes = {409, 503, 429}
    requests_auth_error_status_codes = {401, 403}
    requests_bad_request_error_status_codes = {400}

    for _ in range(try_extract_max_count):
        try:
            output_file_name = Path(output_file).name
            headers['User-Agent'] = f"{code_version} {output_file_name}"
            with requests.request(request_method, url, stream=True, headers=headers, data=payload,
                                  timeout=http_conn_timeout, verify=get_platform_identification_with_fqdn()) as r:
                qualys_headers = get_qualys_headers(r)
                qtbx_lib_logger.logger_info(f"Qualys Headers: {qualys_headers}, HTTP Status Code: {r.status_code}")


                if r.status_code == 200:
                    qtbx_lib_logger.logger_info(f"reading api response and writing to file: {output_file}")
                    with compression_method(output_file, "wb") as f:
                        for chunk in r.iter_content(chunk_size=chunk_size_calc):
                            f.write(chunk)
                elif r.status_code in requests_abort_error_status_codes:
                    message = get_http_error_code_message_v2_api(str(r.status_code))
                    qtbx_lib_logger.logger_warning(f"HTTP USER: {q_username} url: {url}")
                    raise Exception(f"HTTP Status is: {r.status_code}, message: {message}")
                elif r.status_code in requests_concurrency_error_status_codes:
                    time_sleep = 300  # Concurrency Issue or Service Issue, wait 5 min
                    message = get_http_error_code_message_v2_api(str(r.status_code))
                    qtbx_lib_logger.logger_warning(f"HTTP USER: {q_username} url: {url}")
                    raise Exception(f"HTTP Status is: {r.status_code}, message: {message}")
                elif r.status_code in requests_bad_request_error_status_codes:
                    message = get_http_error_code_message_v2_api(str(r.status_code))
                    qtbx_lib_logger.logger_error(f"HTTP USER: {q_username} url: {url}")
                    if isinstance(r.text, str):
                        error_xml_02 = r.text.replace('|', '').replace('\n', '')
                        qtbx_lib_logger.logger_error(f"MESSAGE: {error_xml_02}")
                        exit(1)
                    else:
                        qtbx_lib_logger.logger_error(f"MESSAGE: NO DATA FOUND FOR HTTP 400 ERROR FROM QUALYS.")
                        qtbx_lib_logger.logger_error(f"HTTP USER: {q_username} url: {url}")
                        qtbx_lib_logger.logger_error(f"HTTP {r.status_code}, exiting. message={message}")
                        exit(1)
                elif r.status_code in requests_auth_error_status_codes:
                    message = get_http_error_code_message_v2_api(str(r.status_code))
                    qtbx_lib_logger.logger_error(f"HTTP USER: {q_username} url: {url}")
                    qtbx_lib_logger.logger_error(f"HTTP {r.status_code}, exiting. message={message}")
                    exit(1)
                else:
                    message = get_http_error_code_message_v2_api(str(r.status_code))
                    qtbx_lib_logger.logger_error(f"HTTP USER: {q_username} url: {url}")
                    qtbx_lib_logger.logger_error(f"HTTP {r.status_code}, exiting. message={message}")
                    exit(1)
                return r

        except Exception as e:
            time_sleep = time_sleep + 15
            if time_sleep > 90:
                time_sleep = 300  # Jump to 5 min wait after 3 retries at 30, 60, 90 seconds
            qtbx_lib_logger.logger_warning(f"Warning for extract file: {Path(output_file).name}")
            qtbx_lib_logger.logger_warning(f"Warning {e}")
            qtbx_lib_logger.logger_warning(f"Sleeping for {time_sleep} seconds before next retry.")
            qtbx_lib_logger.logger_warning(
                f"Retry attempt number: {_ + 1} of max retry: {try_extract_max_count}")
            time.sleep(time_sleep)
            continue
        else:
            break  # success
    else:
        qtbx_lib_logger.logger_error(f"Max retries attempted: {try_extract_max_count}")
        qtbx_lib_logger.logger_error(f"extract file: {Path(output_file).name}")
        exit(1)


def get_qualys_portal_version(api_fqdn_server, authorization, qtbx_tool="", message=""):

    url = f"https://{api_fqdn_server}/qps/rest/portal/version"  # Qualys Endpoint
    headers = {
        'X-Requested-With': f'qualystbx_v{qualys_tbx.__version__} {qtbx_tool} QTBXM: {message}',
        'User-Agent': f"qualystbx_v{qualys_tbx.__version__} {qtbx_tool} QTBXM: {message}",
        'Authorization': f'Basic {authorization}'}
    payload = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload,
                                    verify=get_requests_module_tls_verify_status_from_env())

        if response.status_code == 200:
            response_text = str(response.text).replace('\n', ' ')
            qtbx_lib_logger.logger_info(f"qps/rest/portal/version http_response_status_code={response.status_code}, "
                             f"response_text={response_text}")
        else:
            response_text = str(response.text).replace('\n', ' ')
            qtbx_lib_logger.logger_info(f"qps/rest/portal/version http_response_status_code={response.status_code}, "
                             f"response_text={response_text}")

    except Exception as e:
        qtbx_lib_logger.logger_warning(f"qps/rest/portal/version failed with exception: {e}")


def get_platform_version():
    pass

if __name__ == "__main__":
    qtbx_lib_logger.setup_logging_stdout(my_logger_prog_name="qtbx_lib_authentication")
    qtbx_credentials_dict = get_credentials_from_env()
    get_gateway_platform_fqdn(qtbx_credentials_dict['q_api_fqdn_server'])
    get_qualys_portal_version(
        api_fqdn_server=qtbx_credentials_dict['q_api_fqdn_server'],
        authorization=qtbx_credentials_dict['q_base64_credentials'],
        qtbx_tool='qtbx_lib_authentication',
        message='BEGIN',
    )

