import json
import os
from rich.console import Console
from rich.markdown import Markdown

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    console = Console()

    config_path = os.path.join(os.path.dirname(__file__), '../config/resume_config.json')
    config = load_config(config_path)

    with open(os.path.join(os.path.dirname(__file__), 'resume_template.md'), 'r') as file:
        template = file.read()

        resume_md = template.format(**config)
        markdown = Markdown(resume_md)
        console.print(markdown)

if __name__ == "__main__":
    main()