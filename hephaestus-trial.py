import requests
import json
import time
import os

# --- Configuration ---
API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"
JSON_FILE = "facts_database.json"
FETCH_INTERVAL_SECONDS = 60 # Fetch a new fact every 60 seconds

# --- Main Logic ---

def load_facts():
    """Loads the existing facts from the JSON file."""
    if not os.path.exists(JSON_FILE):
        return [] # Return an empty list if the file doesn't exist
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            # Handle empty file case
            if os.path.getsize(JSON_FILE) == 0:
                return []
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️  Error reading {JSON_FILE}: {e}. Starting with an empty list.")
        return []

def save_facts(facts):
    """Saves the list of facts to the JSON file."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(facts, f, indent=4)

def fetch_and_process_fact():
    """Fetches a new fact, checks for duplicates, and saves if it's unique."""
    print("🚀 Fetching a new fact from the API...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        
        # The API provides the fact in the 'text' field
        new_fact_text = response.json().get('text')
        
        if not new_fact_text:
            print("⚠️  API response did not contain a fact. Skipping.")
            return

        print(f"💡 Got fact: '{new_fact_text}'")
        
        # Load existing facts and check for duplicates
        facts_archive = load_facts()
        existing_texts = [fact['text'] for fact in facts_archive]

        if new_fact_text in existing_texts:
            print("🟡 Fact already exists in the database. Skipping.")
        else:
            # Add the new unique fact
            new_fact_entry = {'text': new_fact_text, 'source': response.json().get('source_url')}
            facts_archive.append(new_fact_entry)
            save_facts(facts_archive)
            print("✅ New unique fact added to the database!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: Could not connect to API. {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


# --- Automation Loop ---
if __name__ == "__main__":
    print("--- Digital Fact Collector Started ---")
    print(f"Running automatically. Will fetch a new fact every {FETCH_INTERVAL_SECONDS} seconds.")
    print("Press Ctrl+C to stop the script.")
    
    try:
        while True:
            fetch_and_process_fact()
            print(f"\nSleeping for {FETCH_INTERVAL_SECONDS} seconds... 😴\n")
            time.sleep(FETCH_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n--- Script stopped by user. Goodbye! ---")