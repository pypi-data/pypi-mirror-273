import os

URL = "https://7yqodpilya.execute-api.eu-central-1.amazonaws.com/prod"

if "MOOVS_BUSINESS_API_KEY" in os.environ:
    MOOVS_BUSINESS_API_KEY = os.environ["MOOVS_BUSINESS_API_KEY"]
else:
    raise Exception(
        "API Key not found in environment variables, please set MOOVS_BUSINESS_API_KEY."
    )
