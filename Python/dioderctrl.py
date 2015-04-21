import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request
import requests

PUSHBULLET_API_KEY = ""
SPARK_API_KEY = "0a114cbcc6a50c549da43fa4e53924152ee126c4"
SPARK_DEVICE_ID = "55ff70065075555332471887"

app = Flask(__name__)

@app.route("/")
def index():
    return "Nothing to see here"

@app.route("/send_color", methods=["POST"])
def send_color():
    color = request.form.get('args')
    app.logger.info("Color to send: {}".format(color))
    if color != None:
        headers = {"Authorization":"Bearer {0}".format(SPARK_API_KEY)}
        dataToSend = {"command": color}
        app.logger.info("dataToSend: {}".format(dataToSend))
        r = requests.post("https://api.spark.io/v1/devices/{0}/dioder".format(SPARK_DEVICE_ID),data=dataToSend, headers=headers)
        if r.status_code == requests.codes.ok:
            app.logger.info("Response: {}".format(r.text))
            return "Color sent"
        else:
            return "Error sending color"
    else:
        return "Error sending color"
    
if __name__ == "__main__":
    handler = RotatingFileHandler('dioderctrl.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)