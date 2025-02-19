from dotenv import load_dotenv
import os

from llm.model import Model
from pptx_gen.validator import validate_code
from pptx_gen.generator import generate_file


load_dotenv('../.env')
api_key = os.getenv('OPENAI_API_KEY')

prompt = "сгенерируй очень короткую презентацию про какашки слоненка, максимум 2 слайда."
model_api = Model(api_key)

success, text = model_api.generate_text(prompt)
print(f"generated text:\n{text}\n")

success, slides_with_prompts = model_api.generate_structured_text(initial_prompt=prompt, prompt=text)
print(f"generated slides:\n{slides_with_prompts.model_dump(mode='json')['slides']}\n")

slides = slides_with_prompts.model_dump(mode='json')["slides"]
for i in range(len(slides)):
    if "image_prompt" in slides[i] and slides[i]["image_prompt"] != "":
        image_prompt = slides[i]["image_prompt"]
        success, image_url = model_api.generate_image(image_prompt)

        slides[i]["image_url"] = image_url
        del slides[i]["image_prompt"]

print(f"slides {slides}\n")

success, code = model_api.generate_code(slides)

print(f"generated code:\n{code}\n")

eval = validate_code(code)

print(eval)

if eval:
    success, observe = generate_file(code, slides, "../output.pptx")
    print(success, observe)
