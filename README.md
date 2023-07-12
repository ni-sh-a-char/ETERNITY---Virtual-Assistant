[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)

# ETERNITY - A Virtual Assistant for Task Automation

ETERNITY is a virtual assistant designed to automate various tasks. It can perform actions based on voice inputs and provide assistance in different areas.

## Getting Started

To get started with ETERNITY, follow the instructions below.

### Prerequisites

- Make sure you have Python installed on your system.
- Run the following command in the root folder to install the required dependencies:

```
pip install -r requirements.txt
```

- For Windows users, an additional step is required:
- Install `pipwin` by running the following command:

  ```
  pip install pipwin
  ```

- Install `pyaudio` by executing the following command:

  ```
  pipwin install pyaudio
  ```

### Usage

1. Clone this repository or download the source code.
2. Open a terminal or command prompt and navigate to the root folder of the project.
3. Run the following command to start ETERNITY:

```
python ETERNITY.py
```

4. ETERNITY will now listen for your voice inputs and perform various tasks based on your commands.

## Voice Inputs

ETERNITY responds to the following voice inputs:

- `'hello', 'hi', 'hey', 'hey miss', 'hola', 'hallo'`
- `"what is your name", "tell me your name"`
- `"how are you", "how are you doing"`

You can also use voice inputs to tell ETERNITY your name or change its name:

- `"my name is [your name]"`
- `"Your name should be [new name]"`

### Task Commands

ETERNITY can perform various tasks based on voice inputs. Here are some examples:

- `"what's the time", "tell me the time", "what time is it"`: Retrieves the current time.
- `"search for [query]"`: Performs a Google search for the specified query.
- `"youtube [query]"`: Performs a YouTube search for the specified query.
- `"price of [stock]"`: Retrieves stock price details.
- `"play music"`: Plays music on Spotify.
- `"amazon.com [query]"`: Performs a search on Amazon.
- `"make a note"`: Creates notes.
- `"open insta"`: Opens Instagram.
- `"i want tweets"`: Opens Twitter.
- `"open galiyaara"`: Opens Galiyaara by ni_sh_a.char.
- `"show my time table"`: Displays the image of your time table (stored as "image.jpeg" by default).
- `"weather", "tell me the weather report", "what's the condition outside"`: Retrieves weather conditions.
- `"open my mail", "gmail", "check my email"`: Opens Gmail.
- `"game"`: Plays rock, paper, scissors with the computer.
- `"toss", "flip", "coin"`: Tosses a coin.
- `"plus", "minus", "multiply", "divide", "modulus", "+", "-", "*", "/", "%"`: Performs calculator operations.
- `"capture", "screenshot", "my screen"`: Captures a screenshot of the screen (change the location in the code).
- `"exit", "quit", "goodbye"`: Exits the program.

### E.T.E.R.GPT - ETERNITY with ChatGPT Functionality

ETERNITY incorporates E.T.E.R.GPT, which provides ChatGPT-like functionalities. To use E.T.E.R.GPT, you need to create your own OpenAI key and paste it on line 9 of the E.T.E.R.GPT.py file:

```
openai.api_key = "Paste your OpenAI key"
```

### The ETERNITY AND E.T.E.R.GPT are now integrated and could be used only by pasting the OpenAI key in the ETERNITY.py file
