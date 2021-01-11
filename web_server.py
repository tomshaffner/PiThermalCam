from pi_therm_cam import ThermalCam
from flask import Response, request
from flask import Flask
from flask import render_template
import threading
import datetime as dt
import time, socket, logging, traceback
import cv2
import io

# Set up Logger
logging.basicConfig(filename='pithermcam.log',filemode='a',format='%(asctime)s %(levelname)-8s [%(filename)s:%(name)s:%(lineno)d] %(message)s',level=logging.WARNING,datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)

# initialize the output frame and a lock used to ensure thread-safe exchanges of the output frames (useful when multiple browsers/tabs are viewing the stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to warmup
thermcam = ThermalCam()
time.sleep(2.0)

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
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

@app.route('/localsave')
def localsave():
	# Send the current frame as a jpeg to the browder for saving
	global outputFrame
	print("Saving?")	
	flag , encodedImage = cv2.imencode(".jpg", outputFrame)
	# response=make_response(bytearray(encodedImage))
	# response.headers.set('Content-Type', 'image/jpeg')
	# response.headers.set('Content-Disposition', 'attachment', filename='pic_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ '.jpg')
	# return response

	filename='pic_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ '.jpg'
	return send_file(io.BytesIO(bytearray(encodedImage)),mimetype='image/jpeg',as_attachment=True,attachment_filename=filename)

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

def pull_images():
	global thermcam, outputFrame
	# loop over frames from the video stream
	while True:
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

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip_address=s.getsockname()[0]
	s.close()
	return ip_address

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# start a thread that will perform motion detection
	t = threading.Thread(target=pull_images)
	t.daemon = True
	t.start()

	ip=get_ip_address()
	port=8000

	print(f'Server can be found at {ip}:{port}')

	# start the flask app
	app.run(host=ip, port=port, debug=False,threaded=True, use_reloader=False)
