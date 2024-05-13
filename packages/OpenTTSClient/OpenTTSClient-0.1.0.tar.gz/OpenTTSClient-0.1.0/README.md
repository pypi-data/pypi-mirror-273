# OpenTTSClient

A simple Python client for interacting with the OpenTTS API.

## Features

- Generate speech from text.
- Retrieve available voices and languages.

## Installation

To install OpenTTSClient, simply use pip:

```bash
pip install .
```

## Usage
Here's how you can use OpenTTSClient:

```python
from open_tts_client import OpenTTSClient

client = OpenTTSClient()
response = client.speak_text('espeak:en', 'Hello, world!')
print(response)  # This will output the binary data of the WAV file
```

## Development
To develop OpenTTSClient, install dependencies and set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

# License
This project is licensed under the MIT License - see the LICENSE file for details.