from common.config import get_env_variable_value, get_secret_value


class ProductionConfig:
    """Production application configuration - pulled from task environment."""
    CLIENT_ID = get_env_variable_value('CLIENT_ID', is_mandatory=True)

    QUEUE_URL = get_env_variable_value('CLIENT_SQS_URL', is_mandatory=True)

    SFTP_HOST = get_env_variable_value('SFTP_HOST', is_mandatory=True)
    SFTP_PORT = get_env_variable_value('SFTP_PORT', is_mandatory=True)
    SFTP_USERNAME = get_secret_value('SFTP_USER', is_mandatory=True)
    SFTP_PASSWORD = get_secret_value('SFTP_PASSWORD', is_mandatory=True)

    TEMP_FILE_PATH = '/tmp/sftp_tmp.json'
