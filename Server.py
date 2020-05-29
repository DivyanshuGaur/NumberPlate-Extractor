from flask import Flask,render_template,request,send_file
from flask_cors import CORS
import base64
import cv2
import  random
import os

app=Flask(__name__)

CORS(app)

@app.route('/')
def homepage():

    return '<h1> Server Started </h1>'



@app.route('/index')
def index():
    return '<h1> Index Page </h1>'


@app.route('/gui' ,methods=['GET','POST'])
def gui():

    if(request.method == 'POST'):
        isthisFile = request.files.get('file')
        print(isthisFile.filename)
        isthisFile.save("./" + isthisFile.filename)
        b64=getdata(isthisFile.filename)
        return b64



def getdata(x):

    print(x)
    img = cv2.imread(x)
    cv2.imshow('image',img)
    plate_classifier = cv2.CascadeClassifier('../Resources/haarcascade_russian_plate.xml')
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detect_classifier = plate_classifier.detectMultiScale(gray_scale, 1.1, 10)
    a=random.randint(0,1000)
    for x, y, w, h in detect_classifier:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 155, 120), 4)

        roi = img[y:y + h, x:x + w]

        fn='NP'+str(a)+'.jpg'
        print('fn is ',fn)
        cv2.imwrite(fn, roi)
        for i in range(0, 5):
            k=1
        with open(fn, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return (encoded_string.decode('utf-8'))


if __name__ == '__main__':
    app.run()