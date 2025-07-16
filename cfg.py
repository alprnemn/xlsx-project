from dotenv import load_dotenv,dotenv_values

ENV_PATH = ".env"

load_dotenv()

config = dotenv_values(ENV_PATH)