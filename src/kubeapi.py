
from kubernetes import client
from kubernetes.client.rest import ApiException
from os import getenv
import logging

# read in token automounted from deployment
f = open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r")
token = f.read()

# generate k8s connection config
configuration = client.Configuration()
configuration.host = 'https://kubernetes.default.svc'
configuration.verify_ssl = True
configuration.ssl_ca_cert = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
configuration.debug = False
configuration.api_key = {"authorization":"Bearer "+ token}
client.Configuration.set_default(configuration)
kubeApi = client.CoreV1Api()

# print out for extra debugging info
if getenv("DEBUG", "false").lower() == "true":
    configuration.debug = True
    client.Configuration.set_default(configuration)
    logging.info("K8s config info:")
    logging.info(configuration)

def get_namespace_labels(namespace="default"):
    try:
        ret = kubeApi.read_namespace(namespace)
        return ret.metadata.labels
    except ApiException as e:
        logging.error("K8s connection failed, check service account credentials and settings. Msg:" + e)