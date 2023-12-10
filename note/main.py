#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

PROMPT_TRANSFORM_TO_TWEET="""
convert the following text into an ultra concise tweet
make sure to really condense it down to its essence
it must have the asymptotically highest information to text ratio
if there are details that do not matter to the overall idea
just omit them. do not under any circumstances use language that
does not directly contribute to the information density.
your sole goal is to make the text understandable by anyone
do not assume anything. it must also be neutral and appeal to
anyone. especially if its an idea. but i hope you have the priorities
straight. it is most important to really condense everything down to its
essence.

so here is the input text:
<SEED>
{seed_text}
</SEED>

again, make sure its understandable by anyone.
think of it like a phd student that has to present his findings
to the general population. take a serious step back
consider all of the instructions carefully. be counterfactual and interesting
while maintaining a neutral tone. also write everything in lowercase
and use minimal symbols. the goal is to grow ideas from seeds into beautiful organisms
so please help me out here and give it your best shot
"""

class FilePath(BaseModel):
    path: Path

    @classmethod
    def from_home_dir(cls, subdir: str, file_extension: str):
        home_dir = Path.home()
        dir_path = home_dir / "notes" / subdir
        dir_path.mkdir(parents=True, exist_ok=True)

        highest_num = max(
            (int(p.stem) for p in dir_path.glob(f'*.{file_extension}') if p.stem.isdigit()), 
            default=0
        )

        new_file = dir_path / f"{highest_num + 1}.{file_extension}"
        return cls(path=new_file)

    def open_in_editor(self):
        editor = os.getenv('EDITOR', 'notepad' if os.name == 'nt' else 'vim')
        subprocess.run([editor, str(self.path)])

    def read_content(self):
        with open(self.path, "r") as f:
            return f.read()

    def write_content(self, content: str):
        with open(self.path, "w") as f:
            f.write(content)

# Function to transform seed text to tweet text
def branch_to_tweet(seed_text: str):
    # Assuming ChatPromptTemplate and ChatOpenAI are defined elsewhere
    prompt = ChatPromptTemplate.from_template(PROMPT_TRANSFORM_TO_TWEET)
    model = ChatOpenAI()
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"seed_text": seed_text}) 
    return response

# Main function
def main():
    seed_file = FilePath.from_home_dir('seeds', 'md')
    seed_file.open_in_editor()
    
    seed_text = seed_file.read_content()
    tweet_text = branch_to_tweet(seed_text)

    tweet_file = FilePath.from_home_dir('tweets', 'md')
    tweet_file.path = tweet_file.path.with_name(seed_file.path.name)  # Match the file name
    tweet_file.write_content(tweet_text)
    tweet_file.open_in_editor()

if __name__ == "__main__":
    main()
