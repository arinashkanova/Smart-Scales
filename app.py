from flask import Flask, Response, render_template, request
import random
from webcam import *
from model import *
from VAR import *
from yolov4 import Detector
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    camera.open(2)  #open camera2
    return render_template('index.html')


detector = Detector(gpu_id=0)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/video_feed')
def video_feed():
    #success, frame = camera.read()
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/result')
def result():
    return render_template("result.html")


@app.route('/results')
def results():
    #camera.release()
    get_picture()
    names = get_info_class(detector, PATH)
    label, price = get_cost(names)
    print(label, price)
    return render_template('prediction.html', result = (label, price))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)