# WBE

After many decades of research, we are excited to announce the first whole brain emulator.

To use it:

```python
from wbe import WBE
from PIL import Image
import requests
from io import BytesIO

# URL of the image
url = "https://i.imgflip.com/22zhdm.jpg"

# Fetch the image
response = requests.get(url)
response.raise_for_status()

# Load the image into Pillow
image = Image.open(BytesIO(response.content))

# Initialise emulator
brain = WBE().wakeup()

# Simulate
thought = brain.emulate(image)
print(thought)
# "Where the fuck am I?"
```