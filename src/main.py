from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pprint import pprint
import base64, json

app = FastAPI()


@app.get("/healthz")
def healthz():
    return "OK"

# mutating webhook for modifying pods
@app.post("/mutate/pods")
async def mutating_webhook(request: Request):
    body = await request.json()
    print("Namespace: " + body['request']['namespace'])
    print("Labels:")
    for label in body['request']['object']['metadata']['labels']:
        print("* " + str(label))
    
    samplePatch = [{"op": "replace", "path": "/metadata/labels/devon-test-add", "value": "yay"}]

    jsonResponse = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        'response': {
            'uid': body['request']['uid'],
            'allowed': True,
            'patchType': 'JSONPatch',
            'patch': base64.b64encode(json.dumps(samplePatch).encode("utf-8")).decode("utf-8")
        }
    }
   
    print(jsonable_encoder(jsonResponse))
    return JSONResponse(content=jsonable_encoder(jsonResponse))
