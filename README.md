# screenshot-discord

Takes screenshot when pressed a custom keyboard shortcut and sends it to a discord channel via bot

## Installation

Create a virtual environment using [venv](https://virtualenv.pypa.io/en/latest/#:~:text=virtualenv%20is%20a%20tool%20to,library%20under%20the%20venv%20module.)

```bash
python -m venv <your-env>
source <your-env>/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install discord.py and other packages.

```bash
pip install discord.py keyboard Pillow
```

## Usage

Add your Discord API token before running

```python
TOKEN = ""
```

Add your channel ID here

```python
channel = client.get_channel("")
```

Finally run the python file with root access (required by keyboard module)
```bash
sudo <path-to-your-env>/bin/python3 screenshot.py
```
