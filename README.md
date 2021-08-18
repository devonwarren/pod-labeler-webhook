# Pod Labeler Webhook
**A Kubernetes Mutating Admission Controller Webhook that will copy labels from a namespace into pods automatically**

A [MutatingAdmissionWebhook](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) will inject itself in the admission process to intercept changes in objects. In this case this will look at changes to Pod objects specifically. The webhook will take the pod info in, take the pod's namespace, and call the kubernetes api with a service account to gather the labels defined inside that namespace, and then re-apply (based on the `LABELS` variable) those labels to the pods.

## Setup

### Customizations
Apply customizations to the yaml files inside the **deploy** folder as needed

1. Find and replace all instances of `kube-system` with something else if you want to install in a different namespace
2. Modify the `certificate.yaml` file as needed
   1. Install certmanager and apply the `selfsigned.yaml` (if `selfsigned-issuer` doesn't exist)
   2. Alternatively setup a ClusterIssuer/Issuer using [cert-manager](https://cert-manager.io/docs/concepts/issuer/) and edit the `certificate.yaml` with customizations
   3. Replace `kube-system` with alternative namespace if installing elsewhere
3. Modify the `deployment.yaml` file as needed with the following options
   1. Change environment variables as needed (see [Available Variables below](#available-variables))
   2. Change the replica and resources values as needed depending on how many targeted pods your evironment might have (the defaults are probably fine for anything under 10k)
4. Modify the `mutatingwebhook.yaml` as needed
   1. Remove the `namespaceSelector` lines if you want all pods targeted (careful as this will include itself/kube-system)
   2. Change the `namespaceSelector` to select the namespaces you want to target (see [namespaceSelector docs](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-namespaceselector))

### Apply Kubernetes Files
Apply in the following order after making any needed modifications

```bash
kubectl apply -f certificate.yaml
kubectl apply -f service-account.yaml
kubectl apply -f deployment.yaml
kubectl apply -f mutatingwebhook.yaml
```

## Available Variables
These variables can be set when running the docker image to customize the functionality

| Variable | Default | Description |
| --- | --- | --- |
| **DEBUG** | False | If set to True will enable additional output including a dump of input and output objects for debugging purposes |
| **LABELS** | * | The labels to be copied into pods from their namespaces, if set to '*' will copy all, else can put in multiple values separated by commas |

## Troubleshooting

### Labels are not being applied

1. Check that the pod is up
2. Verify the namespace targeting has been setup correctly
3. Verify the namespace has the labels setup from the `namespaceSelector` (if applicable)
4. Enable `DEBUG` and check the logs

### Check Pod is Up
```bash
kubectl get po -l app=pod-labeler-webhook
```

### Check Logs
Enable the `DEBUG` variable if needed for additional output
```bash
kubectl logs -l app=pod-labeler-webhook
```
