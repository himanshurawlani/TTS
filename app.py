import os
import traceback

from flask import Flask, flash, render_template, request
from google.cloud import texttospeech

# Instantiate a TTS client
client = texttospeech.TextToSpeechClient()
# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Instantiate flask app
app = Flask(__name__)
# Set secret key for flash messages
app.config["SECRET_KEY"] = "df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506"


@app.route("/", methods=["POST"])
def main():
    # Check the request method
    if request.method == "POST":
        txt = request.form["txt"].strip()
        # Check if the user has entered the text
        if not txt:
            flash("Text is required!")
        else:
            try:
                # Set the text input to be synthesized
                synthesis_input = texttospeech.SynthesisInput(text=txt)

                # Perform the text-to-speech request on the text input with the selected
                # voice parameters and audio file type
                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

                # The response's audio_content is binary.
                output_path = os.path.join("static", "output.mp3")
                with open(output_path, "wb") as out:
                    # Write the response to the output file.
                    out.write(response.audio_content)
                    print(f"Audio content written to file {output_path}")

                return render_template("index.html", audio="output.mp3")
            except:
                print(traceback.format_exc())
                return render_template(
                    "index.html",
                    message="Error converting text to audio, please contact support.",
                )

    return render_template("index.html")
