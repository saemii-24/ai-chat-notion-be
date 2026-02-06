from PIL import Image
import pytesseract
import io


def extract_text_from_image(file):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents))

    return pytesseract.image_to_string(image, lang="kor+eng")
