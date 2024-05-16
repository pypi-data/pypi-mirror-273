import json

def beautify_response(response):
    return json.dumps(response, indent=4)