# main_archive.py

import json
import os
import requests

# Define the name of our storage file. Using a constant makes it easy to change later.
FACTS_FILE = "fact_archive.json"
API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"


def fetch_random_fact():
    """Fetches a single random fact from the specified API."""
    print("🌐 Fetching a new fact from the API...")
    try:
        # It's good practice to identify your script with a User-Agent header.
        headers = {'User-Agent': 'OpenImpactLab Fact Collector v1.0'}
        
        # Make the GET request to the API. Timeout is a safeguard.
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        # Raise an error if the request was unsuccessful (e.g., 404 Not Found, 500 Server Error)
        response.raise_for_status()
        
        # Parse the JSON response from the API
        api_data = response.json()
        
        # Create our standardized fact dictionary. This ensures our data format is consistent.
        new_fact = {
            "text": api_data['text'],
            "source": api_data['source_url'] 
        }
        return new_fact

    except requests.exceptions.RequestException as e:
        # Handle network errors (no internet, DNS failure, etc.)
        print(f"❌ Network Error: Could not fetch fact. {e}")
        return None
    except KeyError:
        # Handle cases where the API response doesn't have the 'text' or 'source_url' key.
        print("❌ API Error: The response format was unexpected.")
        return None

def load_facts():
    """Loads the list of facts from the JSON file."""
    # ⚡️ If the file doesn't exist yet (first time running), return an empty list.
    if not os.path.exists(FACTS_FILE):
        return []
    
    # Use a try-except block to handle potential errors, like an empty file.
    try:
        with open(FACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # This happens if the file is empty or corrupted. Start fresh.
        return []

def save_facts(facts):
    """Saves the entire list of facts to the JSON file."""
    # 'w' mode means we overwrite the file with the new, updated list.
    with open(FACTS_FILE, 'w', encoding='utf-8') as f:
        # Use indent=4 for pretty, human-readable JSON.
        json.dump(facts, f, indent=4)

def is_duplicate(new_fact, existing_facts):
    """Checks if a new fact already exists in our list."""
    for fact in existing_facts:
        # We assume the fact's text is the unique part.
        if fact['text'] == new_fact['text']:
            return True # Found a duplicate!
    return False # No duplicates found.

# --- Main Execution ---
# This is where we simulate the process.
if __name__ == "__main__":
    print("🚀 Starting the Fact Archive Manager...")

    # 1. Simulate fetching a new fact. This is what your API call will provide.
    #    In the final project, you'll replace this with your actual API fetching code.
    new_fact = fetch_random_fact()

# 1.5. Proceed only if the fetch was successful.
    if new_fact:
        print(f"✨ Fetched fact: \"{new_fact['text']}\"")
    
    # 2. Load our existing archive.
    print(f"Loading facts from {FACTS_FILE}...")
    my_facts = load_facts()
    print(f"Found {len(my_facts)} facts in the archive.")

    # 3. Check for duplicates before adding.
    print(f"Checking if the new fact is a duplicate...")
    if not is_duplicate(new_fact, my_facts):
        # 4. If it's not a duplicate, add it to our list.
        print("✅ New unique fact found! Adding to archive.")
        my_facts.append(new_fact)
        
        # 5. Save the updated list back to the file.
        save_facts(my_facts)
        print("💾 Archive updated successfully.")
    else:
        print("⚠️ Duplicate fact detected. Not adding to archive.")

    print("\n--- Current Archive ---")
    # Print all facts currently in the archive for verification.
    if my_facts:
        for i, fact in enumerate(my_facts):
            print(f"{i+1}. {fact['text']}")
    else:
        print("Archive is empty.")
    
    print("\n🎯 Process complete.")