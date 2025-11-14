import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "json/creds.json"
from google.cloud import vision
import io
import json
from openai import OpenAI
from pdflatex import PDFLaTeX
import time

google_client = vision.ImageAnnotatorClient()

os.environ["OPENAI_API_KEY"] = "OMITTED"
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
    print("Tex file written")
    pdfl = PDFLaTeX.from_texfile('output/output.tex')
    time.sleep(5)
    print("pdfl generated")
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    if not completed_process:
        print("Big problem")
        exit(0)
    return True

print("Start")

full_extracted_text = ""
filenames = sorted(os.listdir("images"))

for filename in filenames:
    success, extracted_text = extract_text("images/" + filename)
    if success:
        print("Text extracted for " + filename)
        full_extracted_text += extracted_text + "\n"
    else:
        print("No text detected")
print("Extracted text")
if (len(full_extracted_text) < 5):
    exit(0)
print(full_extracted_text)

success, raw_latex = generate_raw_latex(full_extracted_text)
if success:
    print("Raw latex extracted. Generating pdf")
    generate_latex(raw_latex)
else:
    print(raw_latex)
    
for filename in filenames:
    os.remove("images/" + filename)

