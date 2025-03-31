from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import requests
import json
from datetime import datetime, timedelta
from transformers import pipeline



nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
CORS(app)

print("Hello from the backend!")

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


# Example categories (your intents)
candidate_labels = ["music", "sports", "general_irrelevant", "chit-chat", "spam", "off-topic"]

def detect_intent(user_input):
    result = classifier(user_input, candidate_labels)
    intent = result["labels"][0]  # Get the highest scoring label
    return intent


@app.route('/process', methods=['POST'])
def process_input():
    # Extract user input from chat history
    chat_history = request.json.get('input', [])
    user_input = chat_history[-1]['text'] if chat_history else ''  # Get the latest user message
    print(f"User input: {user_input}")
    detected_intent = detect_intent(user_input)
    print(f"Query: {user_input}\nIntent: {detected_intent}\n")


    # Basic intent detection (e.g., event search, filter queries)
    # if "concert" in user_input.lower():
    #     intent = "search_concerts"
    # elif "workshop" in user_input.lower():
    #     intent = "search_workshops"
    # else:
    #     intent = "unknown"
    intent = detected_intent
    print(f"Detected intent: {intent}")
    
    if intent == "spam":
        return jsonify({'result': "That doesn't seem like a valid query. I'm here to help with events—let me know if you're looking for concerts, sports, or workshops!"})
    elif intent == "off-topic":
        return jsonify({'result': "It seems your query isn't related to events. Try asking about concerts, sports, or workshops—I’d be happy to help!"})
    elif intent == "chit-chat":
        return jsonify({'result': "Hi there! I'm here to help you find amazing events. Let me know if you're looking for concerts, sports, or workshops!"})

    # Extract entities
    entities = extract_entities(user_input)
    print(f"Extracted entities: {entities}")

    # Fetch event data based on intent and entities
    events = fetch_events(intent, entities)

    # Generate a user-friendly response
    response_text = generate_response(events)
    print(response_text)
    return jsonify({'result': response_text})
    

def convert_date_range(date_str):
    today = datetime.now()

    if "this weekend" in date_str.lower():
        saturday = today + timedelta((5 - today.weekday()) % 7)
        sunday = saturday + timedelta(days=1)
        return saturday.strftime("%Y-%m-%dT00:00:00Z"), sunday.strftime("%Y-%m-%dT23:59:59Z")

    elif "tomorrow" in date_str.lower():
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%dT00:00:00Z"), tomorrow.strftime("%Y-%m-%dT23:59:59Z")

    elif "today" in date_str.lower():
        return today.strftime("%Y-%m-%dT00:00:00Z"), today.strftime("%Y-%m-%dT23:59:59Z")

    elif "next week" in date_str.lower():
        next_monday = today + timedelta((7 - today.weekday()) % 7)  # Next Monday
        next_sunday = next_monday + timedelta(days=6)               # Following Sunday
        return next_monday.strftime("%Y-%m-%dT00:00:00Z"), next_sunday.strftime("%Y-%m-%dT23:59:59Z")

    return None, None


def fetch_events(intent, entities):
    # Hardcoded API Key
    api_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = "3aGYAiGHFeghCjiwl1SeQpmDyjIo24AY"  # Your Ticketmaster API Key

    # Prepare API parameters
    params = {
        "apikey": api_key,  # Include your API Key in the request
        "keyword": intent.replace("search_", ""),  # Convert intent to search keyword
        "city": entities.get("location", ""),      # Extracted location from the query
        "size": 5                                  # Limit the results to 5 events
    }
    
    print(f"API Parameters: {params}")

    # Handle date filtering if applicable
    if entities.get("date"):
        start_date, end_date = convert_date_range(entities["date"])  # Convert date ranges
        if start_date and end_date:
            params["startDateTime"] = start_date
            params["endDateTime"] = end_date
    
    print(params)
    params.pop("keyword", None)
    params["classificationName"] = intent
    print(params)

    # Make the API request
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extract relevant details from the API response
        events = [
            {
                "name": event["name"],
                "date": event["dates"]["start"]["localDate"],
                "location": event["_embedded"]["venues"][0]["name"] if "_embedded" in event else "Unknown location",
                "url": event.get("url", "No URL available")  # Default to "No URL available"
                
            }
            for event in data.get("_embedded", {}).get("events", [])
        ]
        start_date, end_date = convert_date_range(entities["date"])
        print(f"Start Date: {start_date}, End Date: {end_date}")
        # print(json.dumps(response.json(), indent=2))
        return events
    
    else:
        print(f"Error fetching events: {response.status_code}")
        return []
    


def generate_response(events):
    # Generate a user-friendly response
    if not events:
        return "I couldn’t find any events matching your request. Try specifying a location or date!"
    
    response = "Here are some events you might like:\n"
    return events
    # for event in events:
    #     response += f"- {event['name']} on {event['date']} at {event['location']}\n"
    #     response += f"  [Get Tickets]({event['url']})\n"  # Add URL for tickets
    # return response

def extract_entities(user_input):
    doc = nlp(user_input)
    entities = {"location": None, "date": None}  # Defaults to None
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical Entity
            entities["location"] = ent.text
        elif ent.label_ == "DATE":
            entities["date"] = ent.text
    return entities


if __name__ == '__main__':
    app.run(debug=True)