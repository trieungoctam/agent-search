import os
from llm import GPTAPI
from dotenv import load_dotenv

load_dotenv()

gpt = dict(
    type=GPTAPI,
    model_type="gpt-4o-mini",
    key=os.environ.get('OPENAI_API_KEY', 'YOUR OPENAI API KEY'),
    openai_api_base=os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1/chat/completions'),
)