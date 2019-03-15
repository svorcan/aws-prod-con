from producer.config import ProductionConfig
from producer.data_producer import produce_data

if __name__ == '__main__':
    produce_data(ProductionConfig)
