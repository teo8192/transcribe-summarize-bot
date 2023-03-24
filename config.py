import os

from dotenv import load_dotenv

load_dotenv()

def load_env(env_name) -> str:
    env_var = os.getenv(env_name)
    if not env_var:
        raise ValueError(f'No {env_name} found!')

    return env_var

TOKEN = load_env('DISCORD_TOKEN')

SPEECH_KEY = load_env('SPEECH_KEY')
SPEECH_REGION = load_env('SPEECH_REGION')

TEXT_ANALYTICS_KEY = load_env('TEXT_ANALYTICS_KEY')
TEXT_ANALYTICS_ENDPOINT = load_env('TEXT_ANALYTICS_ENDPOINT')

LANGUAGE = "nb-NO"
