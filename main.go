package main

import (
	"fmt"
	"os"
	"strings"
	apiNote "github.com/m-c-frank/note/api"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: note <message>")
		return
	}


	rawNote := strings.Join(os.Args[1:], " ")
	if rawNote == "" {
		return
	}

	origin, err := os.Getwd()
	if err != nil {
		fmt.Println("Error: ", err)
		return
	}

	apiNote.api()
}
