#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

from model import FilePath

def get_branch_prompt(name: str):
    with open(f"./prompts/{name}.pt", "r") as f:
        return f.read()

def evolve(seed: str, prompt: str) -> str:
    # runs an api call to some magic text to text engine
    prompt_template = ChatPromptTemplate.from_template(prompt)
    model = ChatOpenAI()
    chain = prompt_template | model | StrOutputParser()
    response = chain.invoke({"seed_text": seed})
    return response
    
def branch(seed_text:str, name:str) -> str:
    prompt = get_branch_prompt(name)
    response = evolve(seed_text, prompt)
    return response

def main():
    seed_file = FilePath.from_home_dir('seeds')
    seed_file.open_in_editor()
    
    seed_text = seed_file.read_content()
    tweet_text = branch(seed_text, "tweet")

    tweet_file = FilePath.from_home_dir('tweets')
    tweet_file.path = tweet_file.path.with_name(seed_file.path.name)  # Match the file name
    tweet_file.write_content(tweet_text)
    tweet_file.open_in_editor()

if __name__ == "__main__":
    main()
