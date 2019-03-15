from common.config import get_env_variable_value


class ProductionConfig:
    CLIENT_ID = get_env_variable_value('CLIENT_ID', is_mandatory=True)

    QUEUE_URL = get_env_variable_value('CLIENT_SQS_URL', is_mandatory=True)
