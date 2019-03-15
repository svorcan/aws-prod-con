# AWS Producer-Consumer
Simple AWS demo project with dynamically deployed producer and consumer batch jobs which are communicating via queues. 

It is abstract integration project in which event data is provided as JSON files on SFTP server and it is loaded, processed and sent to another service's API. Basically system would act as adapter between two other systems.

## Producers
Producer tasks are downloading all JSON files from provided SFTP directory, enqueueing them to the Amazon SQS and removing them from SFTP after that.

For simplicity of demo project it is presumed that file names are unique per client (e.g. containing event timestamp) and that another service API is implemented as idempotent.


## Consumers
Consumer tasks are polling Amazon SQS for messages, and each message is read, processed and sent to another service API.


##
#### NOTE: This project is still work in progress, and will be updated with other components as soon as they are implemented!