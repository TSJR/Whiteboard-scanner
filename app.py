import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "json/creds.json"
from google.cloud import vision
import io
import json
from openai import OpenAI
from pdflatex import PDFLaTeX
google_client = vision.ImageAnnotatorClient()

os.environ["OPENAI_API_KEY"] = ""
gpt_client = OpenAI()

chat_data = None
with open("json/chat_data.json") as f:
    chat_data = json.load(f)
    f.close()

def extract_text(img_path):
    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()

    img = vision.Image(content=content)
    response = google_client.text_detection(image=img)
    texts = response.text_annotations
    if texts:
        return True, texts[0].description  
    else:
        return False, ""

def generate_raw_latex(text):
    try:
        completion = gpt_client.chat.completions.create(
            model="gpt-4o",
            store=True,
            messages=[
                {"role": "user", "content": chat_data["initial-command"]},
                {"role": "assistant", "content": "OK"},
                {"role": "user", "content": text}
            ]
        )
        text = completion.choices[0].message.content
        start = text.find("```latex") + 9
        end = text.find("```", start + 1)

        return True, text[start:end]
    except Exception as e:
        return False, str(e)

def generate_latex(raw_latex):
    print(raw_latex)
    with open("output/output.tex", "w") as f:
        f.write(raw_latex)
        f.close()

    pdfl = PDFLaTeX.from_texfile('output/output.tex')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    return True

print("Start")
success, extracted_text = extract_text("images/whiteboard3.png")
if success:
    print("Text extract begin")
    success, raw_latex = generate_raw_latex(extracted_text)
    if success:
        print("Raw latex extracted")
        generate_latex(raw_latex)
    else:
        print(raw_latex)
else:
    print("No text detected")
