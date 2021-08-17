import re, logging
from os import getenv

# evaluate env vars
def parse_envvars():
    # set the logging level based on DEBUG env variable
    if getenv("DEBUG", "false").lower() == "true":
        logging.root.setLevel(logging.DEBUG)

    # parse the labels env variable
    envLabels = getenv("LABELS", "*")
    # allow wildcard all as values
    if envLabels == '*':
        selected_labels = '*'
    # else parse the labels into an array
    else:
        selected_labels = []
        for label in envLabels.split(','):
            # get rid of whitespace
            label = label.strip()
            # only allow alphanumeric label names
            if re.match(r"[0-9a-z\-\.]+$", label) and len(label) < 63:
                selected_labels.append(label)
            else:
                logging.info(f"Label '{label}' doesn't match required regex, discarding")
    
    # return parsed labels
    return {'labels': selected_labels}
    
# return jsonpatch dict
def label_jsonpatch_patch(label, value):
    return {
        "op": "replace",
        "path": "/metadata/labels/" + label,
        "value": value
        }