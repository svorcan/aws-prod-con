from consumer.config import ProductionConfig
from consumer.queue_processor import process_queue

if __name__ == '__main__':
    process_queue(ProductionConfig)
