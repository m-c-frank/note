package api

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"time"
)

func writeFile(note string, repositoryPath string) (string, error) {
	noteFileName := fmt.Sprintf("%s.md", time.Now().Format("2006-01-02_15-04-05"))

	noteFilePath := filepath.Join(repositoryPath, noteFileName)

	if err := os.MkdirAll(repositoryPath, 0755); err != nil {
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

func commitFile(noteFilePath string, repositoryPath string) error {
	absoluteNoteFilePath, err := filepath.Abs(noteFilePath)

	if err != nil {
		fmt.Printf("Error: Unable to get absolute path of file: %s\n", err)
		return err
	}

	hasRepo, err := hasGitRepository(repositoryPath)
	if err != nil {
	    return err
	}
	if !hasRepo {
		cmd := exec.Command("git", "init", ".")
		cmd.Dir = repositoryPath
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		err = cmd.Run()
		if err != nil {
			fmt.Println("Error: ", err)
			return err
		}
	}

	cmd := exec.Command("git", "add", absoluteNoteFilePath)
	cmd.Dir = repositoryPath
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		fmt.Println("Error: Unable to add file to Git staging.")
		return err
	}

	commitMessage := fmt.Sprintf("Addnote: %s", filepath.Base(absoluteNoteFilePath))
	cmd = exec.Command("git", "commit", "-m", commitMessage)
	cmd.Dir = repositoryPath
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		fmt.Println("Error: Unable to commit file.")
		return err
	}

	return err
}


func hasGitRepository(repositoryPath string) (bool, error) {
    // check if the .git directory itself exists
    info, err := os.Stat(filepath.Join(repositoryPath, ".git"))
    if err != nil {
        fmt.Println("No git repo found in directory:", err)
        return false, nil
    }
    // If the stat information is not nil and is a directory, it means a .git directory exists
    if info.IsDir() {
        return true, err
    }
    return false, err
}
