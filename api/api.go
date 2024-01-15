package api

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

func TakeNote(rawnote string, origin string) string {
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
origin: %s
---
`, userName, time.Now().Format(time.RFC3339), origin)
	return frontmatter + rawnote
}

func PersistNote(note string, repositoryPath string) error {
	homeDir := os.Getenv("HOME")
	if homeDir == "" {
		return errors.New("You dont have a $HOME env variable. Or something weird is going on")
	}

	noteFilePath, err := writeFile(note, repositoryPath)

	if err != nil {
		return err
	}

	err = commitFile(noteFilePath, repositoryPath)
	if err != nil {
		return err
	}

	return nil
}

func DetermineRepositoryPath(repositoryPath string) (string, error) {
	if repositoryPath != "" {
		err := os.MkdirAll(repositoryPath, os.ModePerm)
		if err != nil {
			fmt.Println("something is wrong with the repository path: ", repositoryPath)
			return "", err
		}

		fmt.Println("Using this as the repository: ", repositoryPath)
		return repositoryPath, nil
	}

	noteRepository := os.Getenv("PATH_NOTES")
	if noteRepository == "" {
		usrPath, err := os.UserHomeDir()
		if err != nil {
			return "", err
		}
		noteRepository := filepath.Join(usrPath, "notes")
		err = os.Setenv("PATH_NOTES", noteRepository)
		if err != nil {
			return "", err
		}
		return noteRepository, nil
	}

	return noteRepository, nil
}
