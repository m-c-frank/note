package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
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

	note := takeNote(rawNote)

	homeDir := os.Getenv("HOME")
	if homeDir == "" {
		fmt.Println("HOME environment variable is not set")
		return
	}

	subdir := "notes"
	notesDir := filepath.Join(homeDir, subdir)

	if os.Getenv("PATH_NOTES") == "" {
		err := os.Setenv("PATH_NOTES", notesDir)
		if err != nil {
			fmt.Println("Error setting PATH_NOTES:", err)
			return
		}
	}

	noteFilePath, err := writeFile(note)

	if err != nil {
		fmt.Println("Error: Error writing file.")
		return
	}

	err = gitCommit(noteFilePath)
	if err != nil {
		fmt.Println("Error: Error git is having commitment issues.")
		return
	}
}


func takeNote(rawnote string) string {
	userName := os.Getenv("USER")
	if userName == "" {
		userName = "mcfrank"
	}

	frontmatter := fmt.Sprintf(`---
title: note
author: "%s"
date: "%s"
keywords:
abstract:
summary:
graphic:
references: 
origin:
---
`, userName, time.Now().Format(time.RFC3339))
	return frontmatter+rawnote
}

func writeFile(note string) (string, error) {
	noteFileName := fmt.Sprintf("%s.txt", time.Now().Format("2006-01-02_15-04-05"))

	notesDir := os.Getenv("PATH_NOTES")
	noteFilePath := filepath.Join(notesDir, noteFileName)

	if err := os.MkdirAll(notesDir, 0755); err != nil {
	    fmt.Println(err)
	    return "", err
	}

	err := os.WriteFile(noteFilePath, []byte(note), 0644)
	if err != nil {
		fmt.Println("Error: Unable to write the note.")
		return "", err
	}

	fmt.Printf("Note saved to %s\n", noteFilePath)

	return noteFilePath, err
}

func gitCommit(noteFilePath string) error {
	notesDir := os.Getenv("PATH_NOTES")

	absoluteNoteFilePath, err := filepath.Abs(noteFilePath)

	if err != nil {
		fmt.Printf("Error: Unable to get absolute path of file: %s\n", err)
		return err
	}

	cmd := exec.Command("git", "add", absoluteNoteFilePath)
	cmd.Dir = notesDir
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		fmt.Println("Error: Unable to add file to Git staging.")
		return err
	}

	commitMessage := fmt.Sprintf("Addnote: %s", filepath.Base(absoluteNoteFilePath))
	cmd = exec.Command("git", "commit", "-m", commitMessage)
	cmd.Dir = notesDir
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		fmt.Println("Error: Unable to commit file.")
		return err
	}

	return err
}
