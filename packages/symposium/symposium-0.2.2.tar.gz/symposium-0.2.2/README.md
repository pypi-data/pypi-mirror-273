# Symposium
Interactions with multiple language models require at least a little bit of a 'unified' interface. The 'symposium' packagee is an attempt to do that. It is a work in progress and will change without notice. If you need a recording capabilities, install the `grammateus` package and pass an instance of Grammateus/recorder in your calls to connectors.
## Unification
One of the motivations for this package was the need in a unified format for messaging language models, which is particularly useful if you are going to experiment with interactions between them.

The unified standard used by this package is as follows.
### 'System' messages
```python
messages = [
    {"role": "world", "name": "openai", "content": "Be an Antagonist."}
]
```
Name field should be set to 'openai', 'anthropic', 'google_gemini' or 'google_palm'.
For the 'anthropic' name, the last 
'system' message will be used as the 'system' parameter in the request. For palm_messages v1beta3 format this message will be used in the 'context' parameter.
### 'User' messages
```python
messages = [
    {"role": "human", "name": "Alex", "content": "Let's discuss human nature."}
]
```
The utility functions stored in the `adapters` sub-package transform incoming and outgoing messages of particular model from this format to a model-specific format and back from the format of its' response to the following output format. This includes the text synthesis with older (but in)
## Output format
The unified standard used by this package is:
```python
message = {
    "role": "machine", "name": "claude",  
    "content": " ... ", 
    "tags": [{}],   # optional, if in the response, then returned
    "other": [{}]   # optional, if n > 1
}
```
`name` field will be set to 'chatgpt', 'claude', 'gemini' or 'palm'.<br>
Tags are extracted from the text and put into a list. The placeholder for the tags is: (tag_name).<br>
If there are more than one response, the other field will contain the list of the rest (transformed too).
## Anthropic
There are two ways of interaction with Anthropic API, through the REST API and through the native Anthropic Python library with 'client'. If you don't want any dependencies (and uncertainty) use `anthropic_rest` connector. If you want to install this dependency do `pip install symposium[anthropic_native]`.
#### Messages
REST version:
```python
from symposium.connectors import anthropic_rest as ant

messages = [
    {"role": "human", "name": "alex", "content": "Can we change human nature?"}
]
kwargs = {
    "model":                "claude-3-sonnet-20240229",
    "system":               "answer concisely",
    # "messages":             [],
    "max_tokens":           5,
    "stop_sequences":       ["stop", ant.HUMAN_PREFIX],
    "stream":               False,
    "temperature":          0.5,
    "top_k":                250,
    "top_p":                0.5
}
response = ant.claud_message(messages,**kwargs)
```
Native version:
```python
from symposium.connectors import anthropic_native as ant

ant_client = ant.get_claud_client()
messages = [
    {"role": "human", "name": "alex", "content": "Can we change human nature?"}
]
anthropic_message = ant.claud_message(
    client=ant_client,
    messages=messages,
    **kwargs
)
```
#### Completion
Again, there is a REST version and a native version.
REST version:
```python
from symposium.connectors import anthropic_rest as ant

messages = [
    {"role": "human", "name": "alex", "content": "Can we change human nature?"}
]
kwargs = {
    "model":                "claude-instant-1.2",
    "max_tokens":           5,
    # "prompt":               prompt,
    "stop_sequences":       [ant.HUMAN_PREFIX],
    "temperature":          0.5,
    "top_k":                250,
    "top_p":                0.5
}
response = ant.claud_complete(messages, **kwargs)
```
## OpenAI
Import:
```python
from symposium.connectors import openai_rest as oai
```
#### Messages
```python
from symposium.connectors import openai_rest as oai

messages = [
  {"role": "user", "content": "Can we change human nature?"}
]
kwargs = {
    "model":                "gpt-3.5-turbo",
    # "messages":             [],
    "max_tokens":           5,
    "n":                    1,
    "stop_sequences":       ["stop"],
    "seed":                 None,
    "frequency_penalty":    None,
    "presence_penalty":     None,
    "logit_bias":           None,
    "logprobs":             None,
    "top_logprobs":         None,
    "temperature":          0.5,
    "top_p":                0.5,
    "user":                 None
}
responses = oai.gpt_message(messages, **kwargs)
```
#### Completion
```python
from symposium.connectors import openai_rest as oai

prompt = "Can we change human nature?"
kwargs = {
    "model":                "gpt-3.5-turbo-instruct",
    # "prompt":               str,
    "suffix":               str,
    "max_tokens":           5,
    "n":                    1,
    "best_of":              None,
    "stop_sequences":       ["stop"],
    "seed":                 None,
    "frequency_penalty":    None,
    "presence_penalty":     None,
    "logit_bias":           None,
    "logprobs":             None,
    "top_logprobs":         None,
    "temperature":          0.5,
    "top_p":                0.5,
    "user":                 None
}
responses = oai.gpt_complete(prompt, **kwargs)
```
## Gemini
Import:
```python
from symposium.connectors import gemini_rest as gem
```
#### Messages
```python
from symposium.connectors import gemini_rest as gem

messages = [
        {
            "role": "user",
            "parts": [
                {"text": "Human nature can not be changed, because..."},
                {"text": "...and that is why human nature can not be changed."}
            ]
        },{
            "role": "model",
            "parts": [
                {"text": "Should I synthesize a text that will be placed between these two statements and follow the previous instruction while doing that?"}
            ]
        },{
            "role": "user",
            "parts": [
                {"text": "Yes, please do."},
                {"text": "Create a most concise text possible, preferably just one sentence}"}
            ]
        }
]
kwargs = {
    "model":                "gemini-1.0-pro",
    # "messages":             [],
    "stop_sequences":       ["STOP","Title"],
    "temperature":          0.5,
    "max_tokens":           5,
    "n":                    1,
    "top_p":                0.9,
    "top_k":                None
}
response = gem.gemini_content(messages, **kwargs)
```
 
## PaLM
Import:
```python
from symposium.connectors import palm_rest as path
```
#### Completion
```python
from symposium.connectors import palm_rest as path

kwargs = {
    "model": "text-bison-001",
    "prompt": str,
    "temperature": 0.5,
    "n": 1,
    "max_tokens": 10,
    "top_p": 0.5,
    "top_k": None
}
responses = path.palm_complete(prompt, **kwargs)
```
#### Messages
```python
from symposium.connectors import palm_rest as path

context = "This conversation will be happening between Albert and Niels"
examples = [
        {
            "input": {"author": "Albert", "content": "We didn't talk about quantum mechanics lately..."},
            "output": {"author": "Niels", "content": "Yes, indeed."}
        }
]
messages = [
        {
            "author": "Albert",
            "content": "Can we change human nature?"
        }, {
            "author": "Niels",
            "content": "Not clear..."
        }, {
            "author": "Albert",
            "content": "Seriously, can we?"
        }
]
kwargs = {
    "model": "chat-bison-001",
    # "context": str,
    # "examples": [],
    # "messages": [],
    "temperature": 0.5,
    # no 'max_tokens', beware the effects of that!
    "n": 1,
    "top_p": 0.5,
    "top_k": None
}
responses = path.palm_content(context, examples, messages, **kwargs)
```