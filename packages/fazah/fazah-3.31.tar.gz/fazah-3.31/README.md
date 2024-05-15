# Fazah

Fazah is a Python library that enables seamless language translation for interactions with Large Language Models (LLMs). It allows users to communicate with LLMs in any language, ensuring accurate and comprehensive responses by leveraging the vast amount of information available in English on the internet.

## Supported LLMs

Fazah seamlessly integrates with popular LLM APIs, including:

- Anthropic
- OpenAI
- Google Gemini
- And more!

## Installation

To install Fazah, use pip:

```
pip install fazah
```

## Usage

To use Fazah, start by importing the necessary module:

```python
from fazah import Fazah
```

### Using Fazah with Anthropic API

1. Initialize the Anthropic client with your API key:

```python
client = Anthropic(api_key="YOUR_API_KEY")
```

2. Create a function to generate responses using the Anthropic API:

```python
def create_anthropic_llm_model():
    def generate(prompt):
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system="You are a helpful assistant.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        if isinstance(response.content, list):
            response.content = response.content[0].text
        elif hasattr(response.content, 'text'):
            response.content = response.content.text
        return response.content
    return generate
```

3. Create an instance of the Fazah class with the Anthropic LLM model:

```python
llm_model = create_anthropic_llm_model()
fazah = Fazah(llm_model)
```

### Using Fazah with Google Gemini API

1. Set up the Google Gemini API key:

```python
API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=API_KEY)
```

2. Create an instance of the Google Gemini model:

```python
model = genai.GenerativeModel('gemini-pro')
```

3. Create an instance of the LLM model using Google Gemini:

```python
def create_llm_model():
    def generate(prompt):
        response = model.generate_content(prompt)
        return response.text
    return generate
```

4. Create an instance of the Fazah class with the Google Gemini LLM model:

```python
llm_model = create_llm_model()
fazah = Fazah(llm_model)
```

### Using Fazah with OpenAI API

1. Set up the OpenAI API key:

```python
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
client = OpenAI(api_key=OPENAI_API_KEY)
```

2. Create an instance of the OpenAI Chat model:

```python
def create_chatgpt_llm_model():
    def generate(prompt):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    return generate
```

3. Create an instance of the Fazah class with the OpenAI Chat model:

```python
llm_model = create_chatgpt_llm_model()
fazah = Fazah(llm_model)
```

Now you can use the `fazah` object to process text in any language. Fazah will automatically translate the prompt to English, pass it to the respective LLM API, and then translate the generated response back to the original language.

## Key Features

- Automatic translation of user prompts from any language to English
- Leverages the extensive English language resources available on the internet
- Translates LLM responses back into the original language of the user prompt
- Seamless integration with popular LLM APIs
- Enhances the user experience by providing localized interactions
- Enables users to ask complex questions and receive comprehensive responses in their preferred language


## Support

If you encounter any issues or have questions about Fazah, please contact Ajlang5@wisc.edu or wjfoster2@wisc.edu.

---

With Fazah, you can unlock the full potential of LLMs for a global audience, breaking down language barriers and providing an inclusive and accessible experience for all users.