from io import BytesIO, StringIO
from flask import Flask, send_file
from screenshot import Screenshot
from flask import render_template

app = Flask(__name__)

def serve_image(image):
	img_io = BytesIO()
	image.save(img_io, 'JPEG', quality=70)
	img_io.seek(0)
	return send_file(img_io, mimetype='image/jpeg')

@app.route('/')
def index():
	screenshot = Screenshot(target='league of legends', dpi=1.25, max_size=400)
	img = screenshot.take_screenshot()
	print(type(img))
	return serve_image(img)