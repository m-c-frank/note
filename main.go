package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/m-c-frank/note/api"
)

func cli() (string, string, error) {
	if len(os.Args) < 2 {
		fmt.Println("Usage: note <message>")
		return "", "", nil
	}

	rawNote := strings.Join(os.Args[1:], " ")
	fmt.Println("The note i received was: ", rawNote)
	if rawNote == "" {
		fmt.Println("For some reason your note was not saved")
		return "", "", nil
	}

	origin, err := os.Getwd()
	if err != nil {
		return "", "", err
	}
	return rawNote, origin, err
}

func main() {
	rawNote, origin, err := cli()
	if err != nil {
		fmt.Println(err)
		return
	}
	note := api.TakeNote(rawNote, origin)

	homeDir, err := os.UserHomeDir()
	if err != nil {
		fmt.Println(err)
		return
	}

	noteRepository := filepath.Join(homeDir, "notes")

	api.PersistNote(note, noteRepository)
}
