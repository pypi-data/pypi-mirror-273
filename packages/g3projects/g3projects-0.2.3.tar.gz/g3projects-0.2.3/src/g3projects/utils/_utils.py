import os
import re

from jinja2 import Environment


def combine_str(*strings: str) -> str:
    return "\n".join(s for s in strings if s) + '\n'


def remove_multiple_newlines(string: str) -> str:
    return re.sub('\n{3,}', '\n', string).strip()


def format_template(env: Environment, tpl_name: str, **kwargs) -> str:
    template = env.get_template(tpl_name)
    rendered = template.render(kwargs)
    return remove_multiple_newlines(rendered)


def write_to_file(path: str, name: str, contents: str) -> None:
    with open(os.path.join(path, name), 'w', encoding='utf-8') as file:
        file.write(contents)
