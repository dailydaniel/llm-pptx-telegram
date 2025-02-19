from aiogram import types

from src.llm.model import Model
from src.pptx_gen.validator import validate_code
from src.pptx_gen.generator import generate_file


async def process_user_prompt(message: types.Message):
    model_api = Model()

    prompt = message.text

    await message.answer("Шаг 1: Генерация текста презентации...")
    success, text = model_api.generate_text(prompt)
    if not success:
        await message.answer("Ошибка при генерации текста презентации.")
        return

    await message.answer("Шаг 2: Разбиение текста на слайды и составление промптов для ассетов...")
    success, slides_with_prompts = model_api.generate_structured_text(initial_prompt=prompt, prompt=text)
    if not success:
        await message.answer("Ошибка при генерации слайдов и промптов.")
        return

    await message.answer("Шаг 3: Генерация картинок/таблиц (демо)...")
    slides = slides_with_prompts.model_dump(mode='json')["slides"]
    for i in range(len(slides)):
        if "image_prompt" in slides[i] and slides[i]["image_prompt"] != "":
            image_prompt = slides[i]["image_prompt"]
            success, image_url = model_api.generate_image(image_prompt)

            if success:
                slides[i]["image_url"] = image_url
            else:
                slides[i]["image_url"] = ""
            del slides[i]["image_prompt"]

    await message.answer("Шаг 4: Генерация Python-кода для PPTX...")
    success, code = model_api.generate_code(slides)
    if not success:
        await message.answer("Ошибка при генерации кода.")
        return

    await message.answer("Шаг 5: Исполнение кода. Создаём PPTX...")
    eval = validate_code(code)

    if eval:
        success, observe = generate_file(code, slides, "output.pptx")
    else:
        await message.answer("Ошибка при исполнении кода.")
        return

    await message.answer("Шаг 6: Отправка PPTX файла...")
    try:
        await message.answer_document(open("output.pptx", "rb"), caption="Презентация готова!")
    except Exception as e:
        await message.answer(f"Ошибка при отправке PPTX: {e}")
