# -*- coding: utf-8 -*-
#!/usr/bin/python3
##################################
# Flask web server for MLX90640 Thermal Camera w Raspberry Pi
# If running directly, run from root folder, not pithermalcam folder
##################################
try:  # If called as an imported module
	from pithermalcam import pithermalcam
except:  # If run directly
	from pi_therm_cam import pithermalcam
from flask import Response, request
from flask import Flask
from flask import render_template
import threading
import time, socket, logging, traceback
import cv2

# Set up Logger
logging.basicConfig(filename='pithermcam.log',filemode='a',
					format='%(asctime)s %(levelname)-8s [%(filename)s:%(name)s:%(lineno)d] %(message)s',
					level=logging.WARNING,datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)

# initialize the output frame and a lock used to ensure thread-safe exchanges of the output frames (useful when multiple browsers/tabs are viewing the stream)
outputFrame = None
thermcam = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

#background processes happen without any refreshing (for button clicks)
@app.route('/save')
def save_image():
	thermcam.save_image()
	return ("Snapshot Saved")

@app.route('/units')
def change_units():
	thermcam.use_f = not thermcam.use_f
	return ("Units changed")

@app.route('/colormap')
def increment_colormap():
	thermcam.change_colormap()
	return ("Colormap changed")

@app.route('/colormapback')
def decrement_colormap():
	thermcam.change_colormap(forward=False)
	return ("Colormap changed back")

@app.route('/filter')
def toggle_filter():
	thermcam.filter_image=not thermcam.filter_image
	return ("Filtering Toggled")

@app.route('/interpolation')
def increment_interpolation():
	thermcam.change_interpolation()
	return ("Interpolation Changed")

@app.route('/interpolationback')
def decrement_interpolation():
	thermcam.change_interpolation(forward=False)
	return ("Interpolation Changed Back")

@app.route('/exit')
def appexit():
	global thermcam
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	thermcam = None
	return 'Server shutting down...'

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

def get_ip_address():
	"""Find the current IP address of the device"""
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip_address=s.getsockname()[0]
	s.close()
	return ip_address

def pull_images():
	global thermcam, outputFrame
	# loop over frames from the video stream
	while thermcam is not None:
		current_frame=None
		try:
			current_frame = thermcam.update_image_frame()
		except Exception:
			print("Too many retries error caught; continuing...")
			logger.info(traceback.format_exc())

		# If we have a frame, acquire the lock, set the output frame, and release the lock
		if current_frame is not None:
			with lock:
				outputFrame = current_frame.copy()

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

def start_server(output_folder:str = '/home/pi/pithermalcam/run_data/'):
	global thermcam
	# initialize the video stream and allow the camera sensor to warmup
	thermcam = pithermalcam(output_folder=output_folder)
	time.sleep(0.1)

	# start a thread that will perform motion detection
	t = threading.Thread(target=pull_images)
	t.daemon = True
	t.start()

	ip=get_ip_address()
	port=8000

	print(f'Server can be found at {ip}:{port}')

	# start the flask app
	app.run(host=ip, port=port, debug=False,threaded=True, use_reloader=False)


# If this is the main thread, simply start the server
if __name__ == '__main__':
	start_server()
