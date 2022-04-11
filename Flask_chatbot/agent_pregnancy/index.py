from flask import Flask, request, jsonify, render_template
import os
from google.cloud import dialogflow
import requests
import json
import pusher

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:/Documents/TDP/Flask_chatbot/travel_assistance/prototipo-agent-b0b235d919bb.json"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def list_intents(project_id):
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    intents = intents_client.list_intents(request={"parent": parent})

    for intent in intents:
        intent_object = {"name": intent.name,
        "display_name":intent.display_name, 
        "action":intent.action,
        "root_followup_intent":intent.root_followup_intent_name}
        #return intent.display_name
        return intent_object
        
        #print("=" * 20)
        #print("Intent name: {}".format(intent.name))
        #print("Intent display_name: {}".format(intent.display_name))
        #print("Action: {}\n".format(intent.action))
        #print("Root followup intent: {}".format(intent.root_followup_intent_name))
        #print("Parent followup intent: {}\n".format(intent.parent_followup_intent_name))

        #print("Input contexts:")
        #for input_context_name in intent.input_context_names:
        #    print("\tName: {}".format(input_context_name))

        #print("Output contexts:")
        #for output_context in intent.output_contexts:
        #    print("\tName: {}".format(output_context.name))


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    #print("Session path: {}\n".format(session))

    #for text in texts:
    if texts:
        #text_input = dialogflow.TextInput(text=text, language_code=language_code)
        text_input = dialogflow.TextInput(text=texts, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        return response.query_result.fulfillment_text

        #print("=" * 20)
        #print("Query text: {}".format(response.query_result.query_text))
        #print(
        #    "Detected intent: {} (confidence: {})\n".format(
        #        response.query_result.intent.display_name,
        #        response.query_result.intent_detection_confidence,
        #    )
        #)
        #print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))


#PROBAR EN POSTMAN

@app.route('/get_intent', methods=['GET'])
def list_intent():
    project_id = "prototipo-agent"
    intent_object = list_intents(project_id)
    #intent_name = {"name": name}
    return jsonify(intent_object)
#------------------------------------------------------

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    print(message)
    #project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    project_id ="prototipo-agent"
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'es')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)

# run Flask app
if __name__ == "__main__":
    app.run()