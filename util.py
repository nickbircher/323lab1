import base64

def bytes_to_hex(byte_string):
    hex_string = byte_string.hex()
    return hex_string

def bytes_to_base64(byte_string):
    base64_string = base64.b64encode(byte_string).decode("utf-8")
    return base64_string

def hex_to_bytes(hex_string):
    byte_string = bytes.fromhex(hex_string)
    return byte_string

def base64_to_bytes(base64_string):
    byte_string = base64.b64decode(base64_string)
    return byte_string
