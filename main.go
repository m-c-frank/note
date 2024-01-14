package main

import (
	"fmt"
	"os"
	"strings"
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

	api(rawNote, origin)
}
