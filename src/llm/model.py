from openai import OpenAI
from pydantic import BaseModel
# from enum import Enum

from .prompts import SYSTEM_PROMPT_GENERATE_TEXT, SYSTEM_PROMPT_SPLIT_SLIDES, SYSTEM_PROMPT_GENERATE_CODE


class Slide(BaseModel):
    title: str
    content: str
    image_prompt: str


class Slides(BaseModel):
    slides: list[Slide]


class Model:
    def __init__(self, api_key: str | None  = None):

        if not api_key:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")

        self.client = OpenAI(api_key=api_key)

    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.3,
        model: str = "gpt-4o"
    ) -> tuple[bool, str | None]:
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT_GENERATE_TEXT},
                {"role": "user", "content": prompt},
            ]
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return True, response.choices[0].message.content
        except Exception as e:
            return False, str(e)

    def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3"
    ) -> tuple[bool, str | None]:
        try:
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return True, response.data[0].url

        except Exception as e:
            return False, str(e)

    def generate_structured_text(
        self,
        initial_prompt: str,
        prompt: str,
        temperature: float = 0.3,
        model: str = "gpt-4o"
    ) -> tuple[bool, str | None]:
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT_SPLIT_SLIDES.format(initial_prompt=initial_prompt)},
                {"role": "user", "content": prompt},
            ]
            completion = self.client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                temperature=temperature,
                response_format=Slides,
            )
            return True, completion.choices[0].message.parsed
        except Exception as e:
            return False, str(e)

    def generate_code(
        self,
        slides,
        model: str = "gpt-4o"
    ) -> tuple[bool, str | None]:
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT_GENERATE_CODE},
                {"role": "user", "content": str(slides)},
            ]
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
            )
            code = response.choices[0].message.content.strip().split('\n')
            if '```python' in code[0] and '```' in code[-1]:
                code = '\n'.join(code[1:-1])
            else:
                return False, "Invalid code format"
            return True, code
        except Exception as e:
            return False, str(e)
