import jwt

def encode_jwt(payload):
    return jwt.encode(payload, "secret", algorithm="HS256")

def decode_jwt(encoded_jwt):
    return jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])