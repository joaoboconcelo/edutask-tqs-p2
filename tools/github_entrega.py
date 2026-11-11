"""Operações GitHub autorizadas, com credenciais somente em memória."""
import argparse
import json
import os
import subprocess
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://api.github.com'
REPO = '/repos/joaoboconcelo/edutask-tqs-p2'


def session():
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
    result = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n',
                            capture_output=True, text=True, env=env, check=False)
    credentials = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    token = credentials.get('password')
    if not token:
        raise RuntimeError('Nenhuma credencial GitHub disponível no gerenciador; autenticação necessária.')
    client = requests.Session()
    client.headers.update({'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
                           'X-GitHub-Api-Version': '2022-11-28'})
    return client


def request(client, method, path, payload=None):
    response = client.request(method, BASE + path, json=payload, timeout=40)
    if not response.ok:
        raise RuntimeError(f'GitHub HTTP {response.status_code}: {response.json().get("message", "erro sem detalhe")}')
    return response.json() if response.content else {}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['status', 'runs', 'issues', 'pulls', 'post', 'patch', 'get', 'download'])
    parser.add_argument('--path')
    parser.add_argument('--file')
    parser.add_argument('--output')
    args = parser.parse_args()
    client = session()
    if args.action == 'status':
        repo = request(client, 'GET', REPO)
        result = {k: repo[k] for k in ['full_name', 'html_url', 'default_branch', 'permissions']}
    elif args.action == 'runs':
        data = request(client, 'GET', REPO + '/actions/runs?per_page=20')
        result = [{k: r[k] for k in ['id','name','head_sha','head_branch','event','status','conclusion','html_url']} for r in data['workflow_runs']]
    elif args.action in ['issues', 'pulls']:
        data = request(client, 'GET', REPO + '/' + args.action + '?state=all&per_page=100')
        result = [{k: r.get(k) for k in ['number','title','state','html_url']} for r in data]
    elif args.action in ['post', 'patch']:
        payload = json.loads(Path(args.file).read_text(encoding='utf-8'))
        result = request(client, args.action.upper(), REPO + args.path, payload)
        result = {k: result.get(k) for k in ['number','title','state','html_url','id']}
    elif args.action == 'get':
        result = request(client, 'GET', REPO + args.path)
    else:
        response = client.get(BASE + REPO + args.path, timeout=60)
        response.raise_for_status()
        Path(args.output).write_bytes(response.content)
        result = {'arquivo':args.output, 'bytes':len(response.content)}
    if args.output and args.action != 'download':
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
