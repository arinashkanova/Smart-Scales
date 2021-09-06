import cv2


def get_picture():
    result = True
    while(result):
        ret,frame = camera.read()
        cv2.imwrite("NewPicture.jpg",frame)
        result = False
    camera.release()
    cv2.destroyAllWindows()


def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


camera = cv2.VideoCapture(2)