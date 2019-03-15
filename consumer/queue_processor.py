import boto3
from botocore.exceptions import ClientError
from consumer.exceptions import AdapterError, ServiceAPIError
from consumer.data_adapter import convert_data
from consumer.service_handler import send_data

queue_client = boto3.client('sqs')


def process_queue(config):
    """Read all messages currently stored in SQS and process each of them."""
    while True:
        try:
            response = queue_client.receive_message(QueueUrl=config.QUEUE_URL,
                                                    AttributeNames=['SentTimestamp'],
                                                    MaxNumberOfMessages=1,
                                                    MessageAttributeNames=['All'],
                                                    VisibilityTimeout=30,
                                                    WaitTimeSeconds=10)
        except ClientError as e:
            # TODO: implement actual logging mechanism
            print(f'Failed to receive message from the queue due to: {e}.')
            break
        else:
            messages = response['Messages']

            if not messages or len(messages) == 0:
                break

            for message in messages:
                receipt_handle = message['ReceiptHandle']
                message_body = message['Body']

                is_processed = _process_message(message_body)

                if is_processed:
                    queue_client.delete_message(QueueUrl=config.QUEUE_URL, ReceiptHandle=receipt_handle)


def _process_message(data):
    """Processes single message and returns information whether it completed successfully or not."""
    try:
        adapted_message = convert_data(data)
        send_data(adapted_message)
        return True
    except AdapterError as e:
        # TODO: implement actual logging mechanism
        print(f'Failed to convert message due to: {e}.')
    except ServiceAPIError as e:
        # TODO: implement actual logging mechanism
        print(f'Failed to send message to service due to: {e}.')

    return False

