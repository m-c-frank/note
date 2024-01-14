#!/usr/bin/bash

git clone https://github.com/m-c-frank/makecli
cd makecli
bash ./install.sh
git clone https://github.com/m-c-frank/note
cd note
result=$($HOME/mkcli -name="note" -source="main.go")
rm -rf ./makecli
rm -rf ./note
echo "you can now delete the ./note dir"
