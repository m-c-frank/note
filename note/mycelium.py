import os
from pathlib import Path

from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

API_KEY = os.environ.get("API_KEY", "something")
PATH_NOTES = Path(os.environ.get("PATH_NOTES", "/home/mcfrank/notes/"))


def get_branch_prompt(name: str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    prompt_path = os.path.join(dir_path, 'prompts', f'{name}.pt')
    with open(prompt_path, 'r') as f:
        return f.read()


def get_simple_context(path_notes=PATH_NOTES / "seeds"):
    files = os.listdir(path_notes)
    sorted_files = sorted((int(
        f.split('.')[0]
    ) for f in files if f.endswith('.md')), reverse=True)
    latest_five = [f"{num}.md" for num in sorted_files[-10:-1]]
    concatenated_content = '\n\n'.join(
        open(path_notes / file).read() for file in latest_five
    )
    return concatenated_content


def mutate_simple(seed: str, target: str) -> str:
    prompt = get_branch_prompt(target)
    prompt_template = ChatPromptTemplate.from_template(prompt)
    model = ChatOllama()
    chain = prompt_template | model | StrOutputParser()
    response = chain.invoke({"seed": seed})
    return response


def mutate_simple_context(seed: str, target: str) -> str:
    prompt = get_branch_prompt(target)
    prompt_template = ChatPromptTemplate.from_template(prompt)
    model = ChatOllama()
    chain = prompt_template | model | StrOutputParser()
    response = chain.invoke({"seed": seed, "context": get_simple_context()})
    return response


def mutate(seed: str, mode: str) -> str:
    if mode == "rephrase":
        return mutate_simple_context(seed, mode)
    return mutate_simple(seed, mode)
