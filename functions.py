import qrcode
from cv2 import imdecode
import numpy as np
from json import dumps
from icecream import ic
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import Image

def generate_qr_from_json(data: dict) -> bytearray:
    return qrcode.make(dumps(data))

# def generate_qr_from_id(id_x: str):
#     return img = qrcode.make(str(id_x))

def decode_qr_code(qr_code: bytearray) -> dict:
    img = imdecode(np.frombuffer(qr_code, np.uint8), -1)
    return decode(img)[0].data.decode("UTF-8")

def str_to_datetime(date: str) -> datetime:
    # return datetime.strptime('11/02/21 08:00', '%d/%m/%y %H:%M')
    return datetime.strptime(date, '%d/%m/%y %H:%M')