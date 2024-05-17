import configparser
import logging
import os
import pathlib
import warnings
from typing import Union

logger = logging.getLogger('h5rdmtoolbox')


def _parse_ini_file(zenodo_ini_filename: Union[str, pathlib.Path]):
    if zenodo_ini_filename is None:
        from h5rdmtoolbox import UserDir
        zenodo_ini_filename = UserDir['repository'] / 'zenodo.ini'
    else:
        zenodo_ini_filename = pathlib.Path(zenodo_ini_filename)
    if not zenodo_ini_filename.exists():
        raise FileNotFoundError(f'File {zenodo_ini_filename} not found.')
    return zenodo_ini_filename


def get_api_token(sandbox: bool,
                  zenodo_ini_filename: Union[str, pathlib.Path] = None):
    """Read the Zenodo API token from the environment variable or config file.
    If an environment variable is found, a possibly existing ini file is ignored!"""
    if sandbox:
        env_token = os.environ.get('ZENODO_SANDBOX_API_TOKEN', None)
        # logger.debug('Took token from environment variable ZENODO_SANDBOX_API_TOKEN: %s', env_token)
    else:
        env_token = os.environ.get('ZENODO_API_TOKEN', None)
        # logger.debug('Took token from environment variable ZENODO_API_TOKEN: %s', env_token)

    if env_token is not None:
        # logger.debug('Took zenodo token from environment variable:: %s', env_token)
        env_token = env_token.strip()
        logger.debug(' Took token from environment variable ZENODO_SANDBOX_API_TOKEN.')
        return env_token

    logger.debug('No environment variable found for the zenodo token. Trying to read it from the config file '
                 '%s .' % zenodo_ini_filename)

    zenodo_ini_filename = _parse_ini_file(zenodo_ini_filename)
    if zenodo_ini_filename.exists():
        logger.debug(f'Zenodo ini file found: {zenodo_ini_filename}')

    config = configparser.ConfigParser()
    config.read(zenodo_ini_filename)
    if sandbox:
        try:
            access_token = config['zenodo:sandbox']['access_token']
            logger.debug('Token read successfully.')
        except KeyError:
            access_token = None
            logger.debug('Error reading sandbox token from section "zenodo:sandbox"')
    else:
        try:
            access_token = config['zenodo']['access_token']
            logger.debug('Token read successfully.')
        except KeyError:
            access_token = None
            logger.debug('Error reading sandbox token from section "zenodo"')

    if not access_token:
        warnings.warn(f'No API token found in {zenodo_ini_filename}. Please verify the correctness of the file '
                      f'{zenodo_ini_filename}. The access_token entry must be in the section [zenodo] or '
                      f'[zenodo:sandbox].')
        logger.error('No token read. Neither file nor env variable found.')
    return access_token


def set_api_token(sandbox: bool,
                  access_token: str,
                  zenodo_ini_filename: Union[str, pathlib.Path] = None):
    """Write the Zenodo API token to the config file."""
    zenodo_ini_filename = _parse_ini_file(zenodo_ini_filename)
    config = configparser.ConfigParser()
    config.read(zenodo_ini_filename)
    if sandbox:
        section = 'zenodo:sandbox'
    else:
        section = 'zenodo'
    if section not in config:
        config[section] = {}
    config[section]['access_token'] = access_token
    with open(zenodo_ini_filename, 'w') as f:
        config.write(f)
