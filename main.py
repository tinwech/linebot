from beauty import getBeauty
from collocation import getCollocation
from meme import get_meme
from video import get_video
from weather import getLocalWeather

def handleWebhook(request):
    req = request.get_json()

    responseText = ""
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "Default Welcome Intent":
        responseText = "Hello from a GCF Webhook"
    elif intent == "get-agent-name":
        responseText = "My name is Flowhook"
    elif intent == "getMeme":
        responseText = get_meme()
    elif intent == "getVideo":
        responseText = get_video()
    elif intent == "getBeauty":
        responseText = getBeauty()
    elif intent == "Weather":
        if req["queryResult"]["parameters"]["location"] == "":
            location = '臺北市'
        else:
            location = req["queryResult"]["parameters"]["location"]["city"]
        responseText = getLocalWeather(location)
    elif intent == "collocation":
        vocabulary = req["queryResult"]["queryText"]
        responseText = getCollocation(vocabulary)
    else:
        responseText = f"There are no fulfillment responses defined for Intent {intent}"

    # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
    if intent == "getMeme" or intent == "getBeauty":
        res = {"fulfillmentMessages": [{"image": {"imageUri": responseText},"platform": "LINE"}]}
    else:
        res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}

    return res
