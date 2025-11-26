# main.py

# Import the 'requests' library, which allows us to send HTTP requests to web servers.
import requests

def fetch_random_fact():
    """
    Connects to the useless-facts API, fetches a random fact, and returns it.
    """
    # The URL of the API endpoint we want to get data from.
    # We specify we want a random fact in English, in JSON format.
    api_url = "https://uselessfacts.jsph.pl/random.json?language=en"

    try:
        # Send a GET request to the API URL.
        response = requests.get(api_url)

        # Raise an exception if the request returned an unsuccessful status code (like 404 or 500).
        response.raise_for_status()

        # Parse the JSON response into a Python dictionary.
        data = response.json()

        # Extract the fact text from the dictionary. The key is 'text'.
        fact = data['text']

        # Print the fact to the console.
        print("🎯 Here is your random fact:")
        print(fact)

    except requests.exceptions.RequestException as e:
        # Handle potential network errors (e.g., no internet connection, API is down).
        print(f"⚠️ Error fetching data: Could not connect to the API. Details: {e}")
    except KeyError:
        # Handle cases where the API response format is not what we expect (e.g., 'text' key is missing).
        print("⚠️ Error processing data: The API response format has changed.")

# This block ensures the fetch_random_fact() function is called only when the script is run directly.
if __name__ == "__main__":
    fetch_random_fact()