import requests
import json



class EmotionAI:
    def __init__(self, base_url, api_key, version="v1"):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.version = version
        print(f"EmotionAI client initialized with base URL: {self.base_url}, version: {self.version}")

    def sentiment_injection(self, messages, session_id=None):
        """
        Sends messages to the sentiment_context_injection endpoint
        and returns the server's response.
        """
        endpoint = f"{self.base_url}/{self.version}/chat/sentiment_injection"
        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}
        payload = {
            "messages": messages,
            "session_id": session_id or None
        }

        print(f"Sending request to {endpoint} with payload:")
        print(json.dumps(payload, indent=2))
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            print("Request successful, parsing response.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return {"error": str(e), "status_code": e.response.status_code}
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
            return {"error": "Connection error"}
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
            return {"error": "Timeout"}
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return {"error": "Request error"}

    def pretty_print_response(self, response):
        """
        Pretty prints the JSON response from the server.
        """
        print("API Response:")
        print(json.dumps(response, indent=2))

# This is where you would add any other methods necessary for interacting
# with different endpoints in your API.


    def chat_completions(self, model, messages, session_id=None):
        endpoint = f"{self.base_url}/{self.version}/chat/completions"
        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": messages,
        }
        if session_id:
            payload["session_id"] = session_id

        print(f"Sending request to {endpoint} with payload:")
        print(json.dumps(payload, indent=2))
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
            print("Request successful, parsing response.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        return {"error": "An error occurred while processing the request."}

    def pretty_print_response(self, completion):
        print("Completion response:")
        print(json.dumps(completion, indent=2))





    def analyze_user_text(self, text, user_id):
        endpoint = f"{self.base_url}/{self.version}/analyze_user_text"
        headers = {
            "X-API-Key": self.api_key,
            "X-User-ID": user_id,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text
        }

        print(f"Sending request to {endpoint} with payload:")
        print(json.dumps(payload, indent=2))

        try:
            response = requests.get(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            print("Request successful, parsing response.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return {"error": str(e), "status_code": e.response.status_code}
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
            return {"error": "Connection error"}
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
            return {"error": "Timeout"}
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return {"error": "Request error"}

