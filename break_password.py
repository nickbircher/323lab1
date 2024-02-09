import requests
from bs4 import BeautifulSoup
from MT19937 import MT19937
from util import base64_to_bytes, bytes_to_base64


def unmix(mt: MT19937, tokens: list[int]) -> None:
    for i in range(mt.n):
        y = tokens[i]
        y ^= (y >> mt.l)
        y ^= (y << mt.t) & mt.c
        y ^= ((y <<  mt.s) & mt.b) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
        y ^= (y >> mt.u) ^ (y >> 22)
        mt.MT[i] = y
    mt.index = 624


def request_password_reset_tokens(username) -> list[int]:
    tokens = []
    for _ in range(78):
        resp = requests.post("http://localhost:8080/forgot", data={"user": username})
        soup = BeautifulSoup(resp.text, "html.parser")
        token = soup.find("font").text.split("token=")[1]
        decoded_token = base64_to_bytes(token).decode("utf-8")
        tokens.extend([int(i) for i in decoded_token.split(":")])
    return tokens


def break_password_reset() -> None:
    username = input("username: ")
    password_reset_tokens = request_password_reset_tokens(username)

    dummy_seed = 0
    mt = MT19937(dummy_seed.to_bytes(4, byteorder="big"))
    unmix(mt, password_reset_tokens)
    token_parts = [str(mt.extract_number()) for _ in range(8)]
    token = ":".join(token_parts).encode("utf-8")
    print("http://localhost:8080/reset?token=" + bytes_to_base64(token))
    

def main():
    break_password_reset()


if __name__ == "__main__":
    main()