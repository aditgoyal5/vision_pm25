# from arduino.app_utils import App
# import time

# def loop():
#     time.sleep(1)

# App.run(user_loop=loop)

from arduino.app_utils import App, Bridge
import time

def loop():
  try:
    pm25 = int(Bridge.call("get_pm25"))
    pm25_smooth = int(Bridge.call("get_pm25_smooth"))
    frames = int(Bridge.call("get_frames"))
    errors = int(Bridge.call("get_errors"))
    bytes_rx = int(Bridge.call("get_bytes"))

    print(
      "PM2.5:", pm25,
      "| PM2.5_smooth:", pm25_smooth,
      "| Frames:", frames,
      "| Errors:", errors,
      "| Bytes:", bytes_rx
    )
  except Exception as e:
    print("Bridge error:", e)

  time.sleep(2)

App.run(user_loop=loop)