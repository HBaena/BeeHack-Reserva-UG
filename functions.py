import qrcode
from PIL import Image
from cv2 import QRCodeDetector
from cv2 import imdecode
import numpy as np
from json import dumps
from icecream import ic

def generate_qr_from_json(data: dict) -> bytearray:
    ic(dumps(data))
    return qrcode.make(dumps(data))

# def generate_qr_from_id(id_x: str):
#     return img = qrcode.make(str(id_x))

def decode_qr_code(qr_code: bytearray) -> dict:
    decoder =QRCodeDetector()
    decoded = imdecode(np.frombuffer(qr_code, np.uint8), -1)
    response, _, _ = decoder.detectAndDecode(decoded)
    (response)
    return response
