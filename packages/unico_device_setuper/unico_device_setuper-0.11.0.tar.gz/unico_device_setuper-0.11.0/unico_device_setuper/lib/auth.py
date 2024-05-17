import contextlib
import getpass
import json
import sys

import keyring
import keyring.errors
import pydantic
import slugify

from unico_device_setuper.lib import cnsl, unitech, utils


class Credentials(pydantic.BaseModel):
    username: str
    password: str


KEYRING_CREDENTIALS_KEY = 'unitech_credentials'


def get_credentials():
    encoded_credentials = keyring.get_password(utils.APP_NAME, KEYRING_CREDENTIALS_KEY)
    if encoded_credentials is not None:
        with contextlib.suppress(pydantic.ValidationError):
            return Credentials.model_validate_json(encoded_credentials)

    username = cnsl.print_blue('Connexion à votre compte Unico:')
    username = input("Nom d'utilisateur: ")
    password = getpass.getpass('Mot de passe: ')
    cnsl.print('')

    credentials = Credentials(username=username, password=password)
    keyring.set_password(utils.APP_NAME, KEYRING_CREDENTIALS_KEY, credentials.model_dump_json())
    return credentials


def clear_credentials():
    with contextlib.suppress(keyring.errors.PasswordDeleteError):
        keyring.delete_password(utils.APP_NAME, KEYRING_CREDENTIALS_KEY)


def choose_client(clients: list[unitech.LoginChooseResponseClientsItem], name: str | None):
    if name is None:
        cnsl.print_blue('Chosir un client:')
        client = cnsl.print_choose(clients, prompt='Client: ', formater=lambda c: c.name.strip())
        cnsl.print()
        return client

    slugified_name = slugify.slugify(name)
    client = next((c for c in clients if slugify.slugify(c.name) == slugified_name), None)
    if client is None:
        cnsl.print_red(f'Aucun client avec le nom [hot_pink3]`{name}`[/hot_pink3]')
        sys.exit()

    return client


async def get_auth_token(unitech_api_base_url: pydantic.HttpUrl, client_name: str | None):
    credentials = get_credentials()
    api_client = unitech.Client(base_url=str(unitech_api_base_url))
    login_first_stage_response = await unitech.post_auth_login.detailed_request(
        client=api_client, body=unitech.LoginPayload(credentials.username, credentials.password)
    )
    if login_first_stage_response.status_code != 200:
        clear_credentials()
        error_message = 'Erreur inconnue'
        with contextlib.suppress(json.JSONDecodeError, KeyError):
            error_message = json.loads(login_first_stage_response.content)['displayMessage']
        cnsl.print_red(f'{error_message}')
        sys.exit()

    assert isinstance(login_first_stage_response.parsed, unitech.LoginChooseResponse)

    client = choose_client(login_first_stage_response.parsed.clients, name=client_name)
    login_second_stage_response = await unitech.post_auth_login.request(
        client=api_client,
        body=unitech.LoginPayload(credentials.username, credentials.password, id_client=client.id),
    )
    assert isinstance(login_second_stage_response, unitech.LoginTokenResponse)
    return login_second_stage_response.access_token
