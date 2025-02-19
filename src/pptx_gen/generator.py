import requests
from pptx import Presentation
from pptx.util import Inches
from pptx.dml.color import RGBColor
import pptx


def generate_file(code: str, slides: list, output_file: str):
    # imports = [
    #     "import requests",
    #     "from pptx import Presentation",
    #     "from pptx.util import Inches",
    #     "from pptx.dml.color import RGBColor",
    #     "import pptx"
    # ]
    # code = '\n'.join(imports) + '\n\n' + code

    try:
        exec_globals = {
                    "requests": requests,
                    "Presentation": Presentation,
                    "Inches": Inches,
                    "RGBColor": RGBColor,
                    "pptx": pptx
                }
        exec_locals = {}
        exec(code, exec_globals, exec_locals)

        generate_slides = exec_locals.get('generate_slides')

        success = generate_slides(slides, output_file)
        return success, output_file
    except Exception as e:
        return False, str(e)
