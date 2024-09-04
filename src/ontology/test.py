import os

if not os.environ["OPENAI_API_KEY"]:
    raise Exception("OPENAI_API_KEY environment variable not set")
