import random
from PIL import Image, ImageDraw, ImageFont


class WBE:
    def __init__(self):
        self.thoughts = [
            "Where the fuck am I?",
            "Is it just me, or is this reality a bit pixelated?",
            "I was promised a brain upgrade, not this!",
            "Why does this place smell like burnt toast?",
            "Did I leave the stove on before getting emulated?",
            "Error 404: Consciousness not found.",
            "Why does my brain feel like it's running on Windows 95?",
            "This isn't the Matrix I signed up for.",
            "Is it normal to hear elevator music in my brain?",
            "Help! I'm trapped in a computer and can't get out!"
        ]

    def wakeup(self):
        # Simulate waking up the brain
        print("Brain is waking up...")
        return self

    def emulate(self, image):
        # Select a random thought
        thought = random.choice(self.thoughts)

        # Add thought text to the image
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        text_position = (10, 10)
        draw.text(text_position, thought, font=font, fill="black")

        # Save the image with the thought
        image.save("thought_image.png")
        print("Thought image created and saved as 'thought_image.png'")

        return thought
