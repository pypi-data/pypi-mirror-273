import requests
import yaml
import os
import json
from .config import delete_cluster, list_clusters
from rich.console import Console

ROOT_PATH = "api/v1"

ENV_ENDPOINT = 'KETA_SERVICE_ENDPOINT'
ENV_TOKEN = 'KETA_SERVICE_TOKEN'

AUTH_FILE_PATH = '~/.keta/config.yaml'

console = Console()


def do_login(name, endpoint, token):
    # Attempt to access the endpoint
    response = requests.get(
        endpoint, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        # Ensure the configuration directory exists
        config_dir = os.path.expanduser('~/.keta')
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, 'config.yaml')
        # Save login information to the configuration file
        config = []
        with open(config_path, 'a', encoding='utf-8'):
            pass

        with open(config_path, 'r+', encoding='utf-8') as f:
            data = f.read()
            if data:
                config = yaml.safe_load(data)

            if name not in [c['name'] for c in config]:
                for item in config:
                    item['default'] = False
                config.append({'name': name, 'endpoint': endpoint, 'token': token, 'default': True})
            # yaml.dump(config, f)
            f.seek(0)
            f.write(yaml.dump(config))
        console.print("[green]Login successful, information saved.[/green]")
    else:
        console.print("[red]Login failed, please check your endpoint and token.[/red]")


def do_logout(name=None):
    # Delete the configuration file

    clusters = list_clusters()
    if not clusters:
        console.print("[red]You are not logged in or already logged out.")
        return
    default_cluster_name = [c for c in clusters if c.get('default')][0].get('name')
    if not name:
        name = default_cluster_name
    if name not in [c['name'] for c in clusters]:
        console.print("[red]You are not logged in or already logged out.")
        return

    delete_cluster(name)
    console.print(f"[green]Logout successful, [bold magenta]{name}[/bold magenta] information deleted.[/green]")


def get_auth():
    # 尝试从环境变量获取endpoint和token
    endpoint = os.getenv(ENV_ENDPOINT)
    token = os.getenv(ENV_TOKEN)

    # 如果环境变量为空，尝试从配置文件读取
    if not endpoint or not token:
        config_path = os.path.expanduser(AUTH_FILE_PATH)
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as file:
                configs = yaml.safe_load(file)
                config = [c for c in configs if c.get('default')][0]
                endpoint = config.get('endpoint')
                token = config.get('token')
        else:
            console.print("[red]No authentication information available.")
            return {}

    # 返回认证信息
    return {'endpoint': endpoint, 'token': token}


def request(method, path, data={}, query_params={}, custom_headers={}):
    # 从getAuth获取认证信息
    auth_info = get_auth()
    if auth_info is None or len(auth_info) == 0:
        console.print("[red]please login first")
        exit(1)

    endpoint = auth_info.get('endpoint')
    token = auth_info.get('token')

    # 确保endpoint已提供
    if not endpoint or not token:
        console.print("[red]Endpoint or token is not provided.")
        return None

    # 拼接完整的URL
    url = ""
    if ROOT_PATH in path:
        url = f"{endpoint.rstrip('/')}/{path.lstrip('/')}"
    else:
        url = f"{endpoint.rstrip('/')}/{ROOT_PATH}/{path.lstrip('/')}"

    # 准备请求头，加入认证Token
    headers = {'Authorization': f"Bearer {token}",
               'Content-Type': "application/json"}
    # 加入任何自定义的请求头
    headers.update(custom_headers)

    if method not in ['get', 'post', 'put', 'delete']:
        raise Exception(f"Invalid method: {method}")

    if isinstance(data, str):
        response = requests.request(
            method, data=data, url=url, params=query_params, headers=headers)
    else:
        response = requests.request(
            method, json=data, url=url, params=query_params, headers=headers)

    if 400 <= response.status_code < 500:
        raise Exception("Bad request", response.status_code, url, method,
                        response.text)
    if 500 <= response.status_code < 600:
        raise Exception("Server error", response.status_code,
                        response.text)
    # 返回响应
    return response


def request_get(path, query_params={}, custom_headers={}):
    return request('get', path, query_params=query_params, custom_headers=custom_headers)


def request_post(path, data={}, query_params={}, custom_headers={}):
    return request('post', path, data=data, query_params=query_params, custom_headers=custom_headers)


def request_put(path, data={}, query_params={}, custom_headers={}):
    return request('put', path, data=data, query_params=query_params, custom_headers=custom_headers)


def request_delete(path, data={}, query_params={}, custom_headers={}):
    return request('delete', path, query_params=query_params, custom_headers=custom_headers)
