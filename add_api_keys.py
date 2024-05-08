from environs import Env
#from google.cloud import dialogflow_v2beta1 as dialogflow

from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def create_api_key(project_id: str, key_name: str) -> Key:
    """
    Creates and restrict an API key. Add the suffix for uniqueness.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to create API keys.

    Args:
        project_id: Google Cloud project id.

    Returns:
        response: Returns the created API Key.
    """
    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = key_name

    # Initialize request and set arguments.
    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    # Make the request and wait for the operation to complete.
    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")
    # For authenticating with the API key, use the value in "response.key_string".
    # To restrict the usage of this API key, use the value in "response.name".
    return response


if __name__ == '__main__':
    #parser = argparse.ArgumentParser()
    #parser.add_argument("keyname", help="How the API key will be displayed")
    #args = parser.parse_args()

    env = Env()
    env.read_env()
    project_id = env.str("PROJECT_ID")
    keyname = 'keynameyes'

    response = create_api_key(project_id, keyname)
    print(response)


