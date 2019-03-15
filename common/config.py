import os
import boto3
from botocore.exceptions import ClientError
from common.exceptions import ConfigError

secrets_client = boto3.client('secretsmanager')


def get_env_variable_value(key, is_mandatory=False):
    """Gets configuration parameter value from environment variables."""
    value = os.environ.get(key)

    if is_mandatory and not value:
        raise ConfigError(f'{key} value must be set.')


def get_secret_value(key, is_mandatory=False):
    """Gets secret configuration parameter value from AWS Secrets Manager."""
    secret_id = get_env_variable_value(key, is_mandatory=is_mandatory)

    try:
        secret_response = secrets_client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        error_code = e.response['Error']['Code']

        if error_code == 'ResourceNotFoundException':
            raise ConfigError(f'Requested secret \'{secret_id}\' was not found.')
        elif error_code == 'InvalidRequestException':
            raise ConfigError(f'Secret request was invalid due to: {e}.')
        elif error_code == 'InvalidParameterException':
            raise ConfigError(f'Secret request had invalid params: {e}.')
        else:
            raise ConfigError(f'Secret request failed due to unknown error: {e}.')
    else:
        if 'SecretString' in secret_response:
            return secret_response['SecretString']
        else:
            return secret_response['SecretBinary']
