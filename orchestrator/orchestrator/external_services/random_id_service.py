import requests


class RandomIdService:
    def __init__(self):
        # Set your API key here
        self.api_key = 'c342c158-71aa-40c9-a0d8-ae2ed2d3fd1f'
        self.base_url = 'https://api.random.org/json-rpc/2/invoke'

    def generate_unique_id(self, num_ids=1, min_val=1, max_val=1000, replacement=False):
        request_data = {
            "jsonrpc": "2.0",
            "method": "generateIntegers",
            "params": {
                "apiKey": self.api_key,
                "n": num_ids,
                "min": min_val,
                "max": max_val,
                "replacement": replacement
            },
            "id": 42
        }

        try:
            response = requests.post(self.base_url, json=request_data)
            response.raise_for_status()
            result = response.json().get("result")

            if result:
                return result["random"]["data"][0] if num_ids == 1 else result["random"]["data"]
            else:
                print("Error in generating random IDs:", response.json().get("error"))
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error in generating random IDs: {e}")
            return []
