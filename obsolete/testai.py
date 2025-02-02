import openai

client = openai.OpenAI(api_key="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")

response = client.models.list()
print(response)
