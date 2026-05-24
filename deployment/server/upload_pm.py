import time
import requests

FILE_PATH = "/home/arduino/vision_env/predicted_pm.txt"

# where to send value
SERVER_URL = "http://127.0.0.1:8000/update"


def read_pm():

    try:
        with open(FILE_PATH, "r") as f:
            return f.read().strip()

    except:
        return None


while True:

    value = read_pm()

    if value:

        try:

            requests.get(
                SERVER_URL,
                params={"pm": value}
            )

            print("sent:", value)

        except Exception as e:

            print("send failed:", e)

    time.sleep(2)