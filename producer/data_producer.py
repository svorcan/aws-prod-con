import re
import boto3
from botocore.exceptions import ClientError
from producer.exceptions import SFTPError
from producer.sftp_handler import SFTPHandler

queue_client = boto3.client('sqs')


def produce_data(config):
    """Download data from SFTP and enqueue it to client's SQS."""
    sftp_handler = SFTPHandler(config)
    data_files = sftp_handler.retrieve_data()

    for data_file in data_files:
        try:
            queue_client.send_message(
                QueueUrl=config.QUEUE_URL,
                MessageBody=data_file.json,
                MessageAttributes={
                    'FileName': data_file.file_name
                },
                MessageGroupId=_get_message_group_id(config.CLIENT_ID)
            )
        except ClientError as e:
            # TODO: implement actual logging mechanism
            print(f'Failed to send file \'{data_file.file_name}\' to the queue due to: {e}.')
            continue
        else:
            try:
                sftp_handler.remove_file(data_file.file_name)
            except SFTPError as e:
                # TODO: implement actual logging mechanism
                print(f'Failed to delete file \'{data_file.file_name}\' from SFTP server due to: {e}.')


def _get_message_group_id(client_id):
    """Generate SQS message group id from client ID."""
    return f'Client{client_id}'
