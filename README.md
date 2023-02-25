# informer 📢

Manage your application transactional messaging.

[![Build](https://github.com/callmewind/informer/actions/workflows/build.yml/badge.svg)](https://github.com/callmewind/informer/actions/workflows/build.yml)
[![codecov](https://codecov.io/github/callmewind/informer/branch/master/graph/badge.svg?token=CVLWDQAYY8)](https://codecov.io/github/callmewind/informer)

##### Flow oriented
Create communication flows from events and change design and messages within the app
- Sending messages to different channels
- Inbox integration
- Grouping messages
- Webhooks

##### Multiple environments and history
Track all the changes and revert to previous states with just a click.
 
##### Channel integration
- Email
- FCM push notifications
- (TODO)IOS Apns push notifications
- (TODO)Webpush
- (TODO)Slack
- (TODO)SMS

##### Observability and metrics
Keep track of all your communications. 
 - (TODO)Channel metrics
 - Flow metrics
 - (TODO)Account metrics
 - (TODO)Export registers

## Arquitecture
This is a standard Django application with normal views, an api with DRF and background jobs.
Key parts of the app are pluggable: 

- Background task processor: currently the only adapter implementation uses [dramatiq](https://dramatiq.io/). Dramatiq itself supports redis, RabbitMQ and Amazon SQS (via a third party package)
- Storage of running communicatino flows and its logs
- Contact storage: currently standard django models
- Stats storage: currently using redis
