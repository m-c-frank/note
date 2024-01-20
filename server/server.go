package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/m-c-frank/note/api"
)

// Note represents the JSON structure for the note
type Note struct {
	Origin  string `json:"origin"`
	Content string `json:"content"`
}

func main() {
	// Create a Gin router
	r := gin.Default()

	// Define the /api/note endpoint
	r.POST("/api/note", func(c *gin.Context) {
		var rawNote Note

		// Bind the JSON to the note struct
		if err := c.BindJSON(&rawNote); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// Print the note content
		fmt.Printf("Received rawNote: %s\n", rawNote.Content)
		fmt.Printf("From origin: %s\n", rawNote.Origin)

		note := api.TakeNote(rawNote.Content, rawNote.Origin)
		repoPath, err := api.DetermineRepositoryPath("")
		if err != nil {
			return
		}
		err = api.PersistNote(note, repoPath)
		if err != nil {
			return
		}
		// Respond
		c.JSON(http.StatusOK, gin.H{"status": "Note received"})
	})

	// Run the server on localhost:3010
	err := r.Run("localhost:3010")
	if err != nil {
		return
	}

}
