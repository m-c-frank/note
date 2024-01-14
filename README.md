# note

this just helps you have all your notes in one location

it also will get a lot of llm features to help you with publishing your ideas

keep an eye out for [mycelium](https://github.com/hyphalnet/mycelium)

## installation

using the install.sh script

```
curl https://github.com/m-c-frank/note/install.sh | sh
```

### if you care:

the install script uses [makecli](https://github.com/m-c-frank/makecli)
its a tool to turn any go program that exposes a runnable main.go into a cli
works on most generic machinest that run linux

```
curl https://github.com/m-c-frank/makecli/install.sh | sh
source ~/.bashrc
git clone https://github.com/m-c-frank/note
cd note
makecli -name note -source main.go
```

## how it works

install note

you just need to type `note` in your command line

and then just type out your idea or thought or whatever you want to note

for now it will just be written to the $HOME/notes directory

they serve as the seeds for whatever comes out of the ideas

## plugins

you can use your notes as inputs to private llms

1. write a function
2. take the note as an input
3. do an arbitrary manipulation to it

stonks
