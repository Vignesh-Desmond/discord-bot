# Discord bot

### Installation

Create a virtual environment using [venv](https://virtualenv.pypa.io/en/latest/#:~:text=virtualenv%20is%20a%20tool%20to,library%20under%20the%20venv%20module.)

```bash
python -m venv <your-env>
source <your-env>/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install discord.py and other packages.

```bash
pip install discord.py keyboard Pillow
```

## Screenshot bot (with Azure Vision)
Takes screenshot when pressed a custom keyboard shortcut, performs OCR via Azure's Vision API and sends it to a discord channel via bot.

### Usage

- Add your Discord API token, Channel ID and Azure Vision API Key and Endpoint to `.env` file. Refer this [example .env file](./.env.example)

- (optional) Modify `take_screenshot()` function to control what kind of screenshot you want.

- (optional) Set a custom keybind in `keyboard.is_pressed(<keybind_here>)`

- (optional) Change duration in `@tasks.loop(seconds=<duration_in_Seconds>)` for recording keypresses.

- Run the python file with root access (required by keyboard module) <br>`sudo <path-to-your-env>/bin/python3 microsoft_screenshot.py`

### Note

If you dont want to use Azure Vision, there is another file [screenshot.py](./screenshot.py) which uses Tesseract OCR. Installation instructions for Tesseract [here](https://www.bl.uk/britishlibrary/~/media/bl/global/early%20indian%20printed%20books/training%20resources/installing%20and%20using%20tesseract%20ocr.pdf)