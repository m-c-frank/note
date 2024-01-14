#!/usr/bin/bash

git clone https://github.com/m-c-frank/makecli
cd makecli
bash ./install.sh
git clone https://github.com/m-c-frank/note
cd note
result=$($HOME/tools/makecli -name="note" -source="main.go")
