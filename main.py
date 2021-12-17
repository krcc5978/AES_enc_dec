import os
import json
import base64
from cipher import Cipher

security_key = 'UqKIO87vsbDEVPD5OikQbEFlGbqxZgrqLES12VpXzyo='
enc_input_path = 'eyJjaXBoZXJ0ZXh0IjoiYjYyMzFhMTI4NGYyNWU3YjYwZDJiNjgyM2NjYjI4YjkzNTI2ZWU5YzU1MGU2ZWM0Y2I2YzdiYmY4NjMzOGRkZDk3OTFjNDM2YzZkNTIzMzI4MTliMzU4ZTc0M2Q1OTU4NDVmYzZlOTBjMGI5ZTRjNmU5YTQxNjg5ZDViMWE2ZGUwNTI0MWI1Njg1NGQwNGMyMjYyMjIzZDM5ZGI0NWU3Y2I2YTgxN2U1ZDQ0MzkxOWU0YTkwNGE0ZGVlNmVlZTU0YzgxYzNjYmRiOGFjNGMzMDgwZGUyZWYxMDNmYjI2MmEiLCJpdiI6ImJjNTkyMzBlOTQzOTY1YjY2YjA5OTU4ZjJmZmUxNWRmM2NhYzc5Mzg1OWE0Nzc0YyJ9'
enc_output_path = 'eyJjaXBoZXJ0ZXh0IjoiMGRiNjU3ZTFmYjJhOGE5OGE4MWVkZjg1MjQ3YjBmNGEzOTdlZTVlOWUwNjhmYTBiMzRlNTU3ODBkZWU5NzNiNzhhZmUxN2FmZmEzNTI5MTc0N2E3NDBhMDdkMWY4YTRjN2JhMmFhOGEyOWEzYmY2YTM3MzBjYjFhNGMzODExZGNiMTQwYmQ0NGNlNGU4MDJlOTc3Yzk5MGEyZDNmMjU3MmY4OTM1YTgxNTM1YmI2YWVhODk1ZTZlOWNmOTNjNGI5M2E3ZWQzMTdhMDQ4NjNkNmM2NzBjYTAyYWZmY2UyMDgiLCJpdiI6IjllZGU5Y2M4YTYyNWY0ZDJjNTJmZjNjNzQyMzA0ZDcxNTgzOWY4ODgzMWQ5NGY4NyJ9'
enc_vott_json = 'eyJjaXBoZXJ0ZXh0IjoiMmZlNWNjNWY3MmU3YWQ2MWYyNzk3ZjE5NmRjM2ViOTJkNzBjNGJmMjM5ODAzMjUwMzQyN2I4Y2FhN2M0MzhkNDFlZjM1M2Y4YTQxOGNiOGY3MDQzNzY5MTdjYTczYTYyIiwiaXYiOiI1OTI5ZGU4YmFkZTYzNmJiYmJkZDE3NDdhNmQ5NmUzMmNjYmQyNjI3YWM5MTc2YmMifQ=='

dec_input_path = {'folderPath': '\\\\192.168.2.129\\camera_data\\アノテーションデータ（保存用）\\test_3\\input'}
dec_output_path = {'folderPath': '\\\\192.168.2.129\\camera_data\\アノテーションデータ（保存用）\\test_3\\output'}


def decrypt_connection(key_security_token: str, encrypted: str) -> dict:
    decoded_json = json.loads(base64.b64decode(encrypted))
    ciphertext = bytes.fromhex(decoded_json["ciphertext"])
    iv = bytes.fromhex(decoded_json["iv"])
    key = base64.b64decode(key_security_token)
    return json.loads(Cipher.aes_decrypt_to_plain(ciphertext, iv, key))


def encrypt_connection(key_security_token: str, decrypted: dict) -> str:
    iv = os.urandom(16) + os.urandom(8)
    key = base64.b64decode(key_security_token)
    ciphertext_hex: str = Cipher.aes_encrypt_to_hex(
        json.dumps(decrypted).encode('utf-8'), iv, key)
    return base64.b64encode(json.dumps({
        "ciphertext": ciphertext_hex,
        "iv": iv.hex(),
    }).encode()).decode()


def main():
    input_path = decrypt_connection(security_key, enc_input_path)
    print(input_path)

    output_path = decrypt_connection(security_key, enc_output_path)
    print(output_path)

    vott_json = decrypt_connection(security_key, enc_vott_json)
    print(vott_json)

    new_enc_input_path = encrypt_connection(security_key, dec_input_path)
    print(new_enc_input_path)

    new_enc_output_path = encrypt_connection(security_key, dec_output_path)
    print(new_enc_output_path)


if __name__ == '__main__':
    main()
