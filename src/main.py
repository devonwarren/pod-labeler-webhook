from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import kubeapi, helpers
import base64, logging, json
from pprint import pprint

app = FastAPI()

# change settings based on env variables
selected_labels = helpers.parse_envvars()['labels']
pprint(selected_labels)

@app.get("/healthz")
def healthz():
    return "OK"

# mutating webhook for modifying pods
@app.post("/mutate/pods")
async def mutating_webhook(request: Request):
    # get response body in array format
    body = await request.json()

    # setup initial vars
    namespace_labels = kubeapi.get_namespace_labels(body['request']['namespace'])
    current_pod_labels = body['request']['object']['metadata']['labels']
    patchset = []

    # loop for all labels selected
    if selected_labels == '*':
        for label, value in namespace_labels:
            # append patches for all nonmatching labels in namespace
            if label not in current_pod_labels or current_pod_labels[label] != value:
                patchset.append(helpers.label_jsonpatch_patch(label, value))
    # loop for only selected labels
    else:
        for label in selected_labels:
            if label in namespace_labels:
                value = namespace_labels[label]
                if label not in current_pod_labels or current_pod_labels[label] != value:
                    patchset.append(helpers.label_jsonpatch_patch(label, value))
            else:
                logging.debug("label '{label}' not set in namespace '{ns}'".format(label=label, ns=body['request']['namespace']))

    # default response
    jsonResponse = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        'response': {
            'uid': body['request']['uid'],
            'allowed': True,
        }
    }

    # add patches is needed
    if len(patchset) > 0:
        jsonResponse['response']['patchType'] = 'JSONPatch'
        jsonResponse['response']['patch'] = base64.b64encode( json.dumps(patchset).encode("utf-8") ).decode("utf-8")

    # return admissionreview json response
    return JSONResponse(content=jsonable_encoder(jsonResponse))
