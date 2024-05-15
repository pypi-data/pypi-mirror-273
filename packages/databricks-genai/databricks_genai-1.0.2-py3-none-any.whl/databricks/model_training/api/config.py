"""Wrapper around MAPI engine in MCLI."""

import logging
import os
from typing import Any, Callable, Tuple, TypeVar

from databricks.sdk import WorkspaceClient
from mcli import config

# pylint: disable=ungrouped-imports
from databricks.model_training.api.exceptions import (DatabricksModelTrainingRequestError, MAPIException,
                                                      MultiMAPIException)

_TCallable = TypeVar('_TCallable', bound=Callable[..., Any])  # pylint: disable=invalid-name

logger = logging.getLogger(__name__)

GENAI_LOCAL_ENV = 'GENAI_LOCAL'

GENAI_TOKEN_OVERRIDE_ENV = 'GENAI_PERSONAL_ACCESS_TOKEN'
GENAI_MAPI_OVERRIDE_ENV = 'GENAI_MAPI_ENDPOINT'

GENAI_MAPI_ENDPOINT_SUFFIX = '/api/2.0/genai-mapi/graphql'


def get_me() -> str:
    """
    Get who is currently logged in.

    Returns:
        str: The name of the current user.
    """

    if os.environ.get(GENAI_LOCAL_ENV, '').lower() == 'true':
        return 'me'

    w = WorkspaceClient()
    me = w.current_user.me().user_name or ''
    logger.debug(f'You are {me}')
    return me


def get_config_from_env() -> Tuple[str, str]:
    """
    Get api key and endpoint from the current MAPI environment.

    Returns:
        Tuple[str, str]: The API key and endpoint.
    """
    if os.environ.get(GENAI_LOCAL_ENV, '').lower() == 'true':
        return 'local', 'local'

    if GENAI_TOKEN_OVERRIDE_ENV in os.environ and GENAI_MAPI_OVERRIDE_ENV in os.environ:
        return os.environ[GENAI_TOKEN_OVERRIDE_ENV], os.environ[GENAI_MAPI_OVERRIDE_ENV]

    w = WorkspaceClient()
    ctx = w.dbutils.entry_point.getDbutils().notebook().getContext()
    api_url = ctx.apiUrl().get()
    api_token = ctx.apiToken().get()
    return api_token, f'{api_url}{GENAI_MAPI_ENDPOINT_SUFFIX}'


def configure_request(func: _TCallable) -> _TCallable:
    """
    Decorator that configures a default retry policy for all MAPI requests

    Args:
        func (Callable[..., Any]): The function that should be retried
    """

    def setup(*args, **kwargs):
        api_token, endpoint = get_config_from_env()

        previous_api_key = os.getenv(config.MOSAICML_API_KEY_ENV)
        previous_endpoint = os.getenv(config.MOSAICML_API_ENDPOINT_ENV)

        logger.debug(f'Setting up MAPI connection with api_token {api_token} and endpoint {endpoint}')

        if os.environ.get('GENAI_LOCAL', '').lower() != 'true':
            os.environ[config.MOSAICML_API_KEY_ENV] = f'Bearer {api_token}'
            os.environ[config.MOSAICML_API_ENDPOINT_ENV] = endpoint

        try:
            res = func(*args, **kwargs)
        except TimeoutError as e:
            raise DatabricksModelTrainingRequestError(f'Timeout connecting to {endpoint}') from e
        except MAPIException as e:
            if isinstance(e, MultiMAPIException):
                e = e.errors[0]
            raise DatabricksModelTrainingRequestError(e.message) from e

        if previous_api_key:
            os.environ[config.MOSAICML_API_KEY_ENV] = previous_api_key
        if previous_endpoint:
            os.environ[config.MOSAICML_API_ENDPOINT_ENV] = previous_endpoint

        return res

    return setup  # pyright: ignore
