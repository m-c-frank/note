package api

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"time"
)

func Call(rawNote string, origin string) (string, error) {
	userName := os.Getenv("USER")
	if userName == "" {
		userName = "mcfrank"
	}

	note := composeNote(rawNote, userName, origin)

	homeDir := os.Getenv("HOME")
	if homeDir == "" {
		return "", errors.New("HOME environment variable is not set")
	}

	subdir := "notes"
	notesDir := filepath.Join(homeDir, subdir)

	if os.Getenv("PATH_NOTES") == "" {
		err := os.Setenv("PATH_NOTES", notesDir)
		if err != nil {
			return "", err
		}
	}

	noteFilePath, err := writeFile(note)
	if err != nil {
		return "", err
	}

	err = gitCommit(noteFilePath)
	if err != nil {
		return "", err
	}
	return "", nil
}

func composeNote(rawnote string, author string, origin string) string {

	frontmatter := fmt.Sprintf(`---
title: note
author: "%s"
date: "%s"
keywords:
abstract:
summary:
graphic:
references: 
origin: %s
---
`, author, time.Now().Format(time.RFC3339), origin)
	return frontmatter + rawnote
}

func writeFile(note string) (string, error) {
	noteFileName := fmt.Sprintf("%s.md", time.Now().Format("2006-01-02_15-04-05"))

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

	if !hasGitRepository(notesDir) {
		cmd := exec.Command("git", "init", ".")
		cmd.Dir = notesDir
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		err = cmd.Run()
		if err != nil {
			fmt.Println("Error: ", err)
			return err
		}
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

func hasGitRepository(path string) bool {
	// check if the .git directory itself exists
	info, err := os.Stat(filepath.Join(path, ".git"))
	if err != nil {
		fmt.Println("No git repo found in directory:", err)
		return false
	}
	// If the stat information is not nil and is a directory, it means a .git directory exists
	if info.IsDir() {
		return true
	}
	return false
}
