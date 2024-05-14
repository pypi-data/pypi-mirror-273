from urllib.parse import urlparse, parse_qs
from .crypto import hmac_sha1
from .crypto import get_machine_code
import uuid


def create_sign_request_string(appid: str, secret: str, method: str, url: str, timestamp: int) -> str:
    pathname = get_url_pathname(url)
    sign_string = f"""
{appid}
{secret}
{get_machine_code()}
{timestamp}
{method}:{pathname}
"""
    return sign_string


def get_url_pathname(url: str) -> str:
    # If the URL does not start with 'http' or '//', prepend 'http://xxx.com'
    if not (url.startswith('http://') or url.startswith('https://') or url.startswith('//')):
        url = f"http://xxx.com{url}"

    # Normalize the URL in case it starts with '//'
    if url.startswith('//'):
        url = 'http:' + url

    # Parse the URL and extract the pathname
    parsed_url = urlparse(url)
    return f"/{parsed_url.path.lstrip('/')}"  # Ensure there is a leading slash


def sign_request(appid: str, secret: str, method: str, url: str, timestamp: int) -> str:
    sign_string = create_sign_request_string(appid, secret, method, url, timestamp)
    sign = hmac_sha1(secret, sign_string)
    return sign


def sign_im(client_type: str, secret: str, appid: str, session_id: str, timestamp: int) -> str:
    machine_code = get_machine_code()
    sign_string = f"""
{client_type}
{secret}
{appid}
{session_id}
{machine_code}
{timestamp}
"""
    return hmac_sha1(secret, sign_string)


def create_session_id() -> str:
    return str(uuid.uuid4())


def create_task_key() -> str:
    return str(uuid.uuid4())
