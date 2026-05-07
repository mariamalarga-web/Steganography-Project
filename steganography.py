import numpy as np
from PIL import Image

# ============================================================
# المشروع: خوارزمية الحقن الرقمي - Steganography Project
# الطالبة: مريم الزماعرة
# الطالب:  حسني النواجعة
# التخصص: أمن سيبراني
# الكلية:  الكلية الذكية للتعليم الحديث
# ============================================================

def encode(image_path, secret_text, output_path):
    img = Image.open(image_path).convert("RGB")
    data = np.array(img)

    binary_message = ""
    length = len(secret_text)
    binary_message += format(length, '032b')
    
    for char in secret_text:
        binary_message += format(ord(char), '08b')

    max_bits = data.size
    if len(binary_message) > max_bits:
        raise ValueError("الصورة صغيرة جداً للنص المطلوب!")

    flat = data.flatten()
    
    for i, bit in enumerate(binary_message):
        flat[i] = flat[i] & 0xFE
        flat[i] = flat[i] | int(bit)

    result = flat.reshape(data.shape)
    output_img = Image.fromarray(result.astype(np.uint8))
    output_img.save(output_path, "PNG")
    print(f"✅ تم الإخفاء وحفظ الصورة في: {output_path}")


def decode(image_path):
    img = Image.open(image_path).convert("RGB")
    data = np.array(img).flatten()

    header_bits = ""
    for i in range(32):
        header_bits += str(data[i] & 1)
    
    message_length = int(header_bits, 2)

    message_bits = ""
    for i in range(32, 32 + message_length * 8):
        message_bits += str(data[i] & 1)

    secret_text = ""
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        secret_text += chr(int(byte, 2))

    print(f"✅ النص المخفي: {secret_text}")
    return secret_text


if __name__ == "__main__":
    encode(
        image_path="original.png",
        secret_text="مريم الزماعرة وحسني النواجعة - تخصص أمن سيبراني - الكلية الذكية للتعليم الحديث",
        output_path="stego_output.png"
    )

    decode("stego_output.png")