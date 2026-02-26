import os
import sys
import click
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Initialize OpenAI client
client = OpenAI()
console = Console()

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def review(file_path):
    """AI-powered code reviewer that provides suggestions and identifies bugs."""
    with open(file_path, 'r') as f:
        code = f.read()

    console.print(f"[bold blue]Reviewing {file_path}...[/bold blue]")

    prompt = f"""
    Review the following code and provide suggestions for improvements, bug detection, and best practice adherence.
    Format your response in Markdown.

    Code:
    ```{os.path.splitext(file_path)[1][1:]}
    {code}
    ```
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {{"role": "system", "content": "You are an expert code reviewer."}},
                {{"role": "user", "content": prompt}}
            ]
        )
        review_text = response.choices[0].message.content
        console.print(Markdown(review_text))
    except Exception as e:
        console.print(f"[bold red]Error during review:[/bold red] {e}")

if __name__ == '__main__':
    review()
