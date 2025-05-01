import ollama

# Your input text
input_text = """
Honeybees are essential pollinators in many ecosystems. They help plants reproduce by transferring pollen between flowers. 
Without bees, many fruits, vegetables, and nuts would become scarce. 
Recent years have seen a decline in bee populations due to habitat loss, pesticides, and disease.
"""

questions = """
  Why are honeybees important to ecosystems?
"""

# Prompt to generate questions
prompt = f"""
Given the following text, answer the questions:

Text:
\"\"\"{input_text}\"\"\"

Questions:
\"\"\"{questions}\"\"\"
"""

# First prompt
messages = [
    {'role': 'user', 'content': prompt}
]
response1 = ollama.chat(model='mistral', messages=messages)
print(response1['message']['content'])

# Add the assistant's reply to the chat
messages.append({'role': 'assistant', 'content': response1['message']['content']})

# Ask a follow-up
messages.append({'role': 'user', 'content': 'Can you give an example of how bees help crops?'})
response2 = ollama.chat(model='mistral', messages=messages)
print(response2['message']['content'])
