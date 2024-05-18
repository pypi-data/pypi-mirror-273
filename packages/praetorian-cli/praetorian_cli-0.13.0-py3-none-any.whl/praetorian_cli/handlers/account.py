import json
import random
from base64 import b64encode

import click

from praetorian_cli.handlers.utils import chariot
from praetorian_cli.handlers.utils import handle_api_error


@chariot.command('accounts')
@click.pass_obj
@handle_api_error
def my_accounts(controller):
    """ Fetch my associated accounts """
    result = controller.my(dict(key=f'#account'))
    for hit in result.get('accounts', []):
        print(f"{hit['key']}")


@chariot.command('integrations')
@click.pass_obj
@handle_api_error
def my_accounts(controller):
    """ Fetch my associated account integrations """
    result = controller.my(dict(key=f'#account'))
    for hit in result.get('accounts', []):
        if "@" not in hit["key"].split("#")[-1]:
            print(f"{hit['key']}")


@chariot.command('unlink')
@click.pass_obj
@handle_api_error
@click.argument('username')
def unlink_account(controller, username):
    """ Unlink a Chariot account from yours """
    result = controller.unlink_account(username=username)
    print(f"{result['key']}")


@chariot.command('add-webhook')
@click.pass_obj
@handle_api_error
def add_webhook(controller):
    """ Authenticated URL for adding assets and risks """
    pin = str(random.randint(10000, 99999))
    controller.link_account(username="hook", config={'pin': pin})
    username = b64encode(controller.keychain.username.encode('utf8'))
    encoded_string = username.decode('utf8')
    encoded_username = encoded_string.rstrip('=')
    print(f'{controller.keychain.api}/hook/{encoded_username}/{pin}')


@chariot.command('link-chariot')
@click.pass_obj
@handle_api_error
@click.argument('username')
def link_account(controller, username):
    """ Link another Chariot account to yours """
    controller.link_account(username, config={})


@chariot.command('link-slack')
@click.pass_obj
@handle_api_error
@click.argument('webhook')
def link_slack(controller, webhook):
    """ Send all new risks to Slack """
    controller.link_account('slack', {'webhook': webhook})


@chariot.command('link-jira')
@click.pass_obj
@handle_api_error
@click.argument('url')
@click.argument('user_email')
@click.argument('access_token')
@click.argument('project_key')
@click.argument('issue_type')
def link_jira(controller, url, user_email, access_token, project_key, issue_type):
    """ Send all new risks to JIRA """
    config = {'url': url, 'userEmail': user_email, 'accessToken': access_token, 'projectKey': project_key,
              'issueType': issue_type}
    controller.link_account('jira', config)


@chariot.command('link-amazon')
@click.pass_obj
@handle_api_error
@click.argument('access_key')
@click.argument('secret_key')
def link_amazon(controller, access_key, secret_key):
    """ Enumerate Amazon for Assets """
    config = {'accessKey': access_key, 'secretKey': secret_key}
    controller.link_account('amazon', config)


@chariot.command('link-azure')
@click.pass_obj
@handle_api_error
@click.argument('appid')
@click.argument('secret')
@click.argument('tenant')
@click.argument('subscription')
def link_azure(controller, appid, secret, tenant, subscription):
    """ Enumerate Azure for Assets """
    config = {'name': appid, 'secret': secret, 'tenant': tenant, 'subscription': subscription}
    controller.link_account('azure', config)


@chariot.command('link-gcp')
@click.pass_obj
@handle_api_error
@click.argument('keyfile')
def link_gcp(controller, keyfile):
    """ Enumerate GCP for Assets """
    config = {}
    with open(keyfile, "r") as f:
        config['default'] = json.loads(f.read())
    controller.link_account('gcp', config)


@chariot.command('link-github')
@click.pass_obj
@handle_api_error
@click.argument('pat')
def link_github(controller, pat):
    """ Allow Chariot to scan your private repos """
    controller.link_account('github', {'pat': pat})


@chariot.command('link-ns1')
@click.pass_obj
@handle_api_error
@click.argument('ns1_api_key')
def link_ns1(controller, ns1_api_key):
    """ Allow Chariot to retrieve zone information from NS1 """
    controller.link_account('ns1', {'ns1_api_key': ns1_api_key})


@chariot.command('link-crowdstrike')
@click.pass_obj
@handle_api_error
@click.argument('client')
@click.argument('secret')
@click.argument('url')
def link_crowdstrike(controller, client, secret, url):
    """ Enumerate Crowdstrike for Assets and Risks """
    config = {'clientID': client, 'secret': secret, 'baseURL': url}
    controller.link_account('crowdstrike', config)
