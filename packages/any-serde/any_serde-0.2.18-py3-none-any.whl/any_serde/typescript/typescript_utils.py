from pathlib import Path
from jinja2 import Template


TYPESCRIPT_MODULE_DIR = Path(__file__).resolve().parent


def load_template(path: Path) -> Template:
    with path.open("rt") as fin:
        return Template(fin.read())
