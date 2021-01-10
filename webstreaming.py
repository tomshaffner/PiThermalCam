from pi_therm_cam import ThermalCam, Motion_Detector
from flask import Response
from flask import Flask, request
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time, socket
import cv2

# initialize the output frame and a lock used to ensure thread-safe exchanges of the output frames (useful when multiple browsers/tabs are viewing the stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to warmup
thermcam = ThermalCam(resize_image=True)
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

#background process happening without any refreshing
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

def detect_motion(frameCount):
	# TODO See if this even works with thermal or is needed. E.g. if an area heats up, will it be detected as motion?
	# grab global references to the video stream, output frame, and lock variables
	global thermcam, outputFrame, lock
	# initialize the motion detector and the total number of frames read thus far
	md = Motion_Detector(accumWeight=0.1)
	total = 0

    # loop over frames from the video stream
	while True:
	# read the next frame from the video stream, resize it, convert the frame to grayscale, and blur it
		frame = thermcam.get_current_raw_image_frame()
		# TODO See if the below can in fact be removed or add them back in
		# frame = imutils.resize(frame, width=400)
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# gray = cv2.GaussianBlur(gray, (7, 7), 0)
		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# if total number of frames has reached sufficient number to construct a reasonable background model, process the frame
		if total > frameCount:
			# detect motion in the image
			motion = md.detect(frame)
			# check to see if motion was found in the frame
			if motion is not None:
				# unpack the tuple and draw the box surrounding the "motion area" on the output frame
				(thresh, (minX, minY, maxX, maxY)) = motion
				cv2.rectangle(frame, (minX, minY), (maxX, maxY),(0, 0, 255), 2)
		
		# update the background model and increment the total number of frames read thus far
		md.update(frame)
		total += 1
		# acquire the lock, set the output frame, and release the lock
		with lock:
			outputFrame = frame.copy()

# def generate():
# 	# grab global references to the output frame and lock variables
# 	global outputFrame, lock
# 	# loop over frames from the output stream
# 	while True:
# 		# wait until the lock is acquired
# 		with lock:
# 			# check if the output frame is available, otherwise skip the iteration of the loop
# 			if outputFrame is None:
# 				continue
# 			# encode the frame in JPEG format
# 			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
# 			# ensure the frame was successfully encoded
# 			if not flag:
# 				continue
# 		# yield the output frame in the byte format
# 		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

def generate():
	while True:
		frame = thermcam.update_image_frame()
		(flag, encodedImage) = cv2.imencode(".jpg", frame)
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip_address=s.getsockname()[0]
	s.close()
	return ip_address

# check to see if this is the main thread of execution
if __name__ == '__main__':

	# start a thread that will perform motion detection
	# t = threading.Thread(target=detect_motion, args=(32,))
	# t.daemon = True
	# t.start()

	ip=get_ip_address()
	port=8000

	print(f'{ip}:{port}')

	# start the flask app
	app.run(host=ip, port=port, debug=True,threaded=True, use_reloader=False)
