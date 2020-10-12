###
### This example creates a mirror maker 2 connector
### The target and source cluster are the same
###

import requests
import sys
import os
import json
import logging
from connect_helper import ConnectHelper

###
# Log settings
###

logging.basicConfig(level=logging.INFO)

###
# Config
###

connect_url = "http://localhost:8083"
connector_name = "new_connector_name"

body = {
    "name": connector_name,
    "connector.class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
    "errors.log.enable": "true",
    "enable.auto.commit": "true",
    "replication.factor": "1",
    "sync.topic.configs.enabled": "false",
    "sync.topic.acls.enabled": "false",
    "checkpoints.topic.replication.factor": "1",
    "heartbeats.topic.replication.factor": "1",
    "offset-syncs.topic.replication.factor": "1",
    "topics": "testtopic",
    "tasks.max": "1",
    "key.converter": "org.apache.kafka.connect.converters.ByteArrayConverter",
    "value.converter": "org.apache.kafka.connect.converters.ByteArrayConverter",
    "source.cluster.bootstrap.servers": "localhost:9092",
    "source.cluster.alias": "source",
    "target.cluster.bootstrap.servers": "localhost:9092",
    "target.cluster.alias": "target",
}

###
# Prepare HTTP session
###
s = requests.Session()
s.verify = ca_cert
s.auth = (connect_username, connect_password)

###
# Main
###

connect = ConnectHelper(s, connect_url)
connect.connector.name = connector_name

logging.info(f"Retrieve all connectors before change:")
connectors_before_change = connect.get_connectors()
logging.info(json.dumps(connectors_before_change.json(), indent=2))

if connector_name in connectors_before_change.json():
    logging.info(f"Configuration of {connector_name} before change:")
    body_before_change = connect.connector.get_remote_config().json()["config"]
    logging.info(json.dumps(body_before_change, indent=2))
else:
    logging.info(f"Connector {connector_name} doesn't exist yet and will be created")

logging.info(f"Upsert {connector_name} connector...")
connect.connector.put(body)
connect.connector.poll_status()

logging.info(f"Configuration of {connector_name} after change:")
body_after_change = connect.connector.get_remote_config().json()["config"]
logging.info(json.dumps(body_after_change, indent=2))

logging.info("Retrieve all connectors after change:")
r = connect.get_connectors()
logging.info(json.dumps(r.json(), indent=2))
