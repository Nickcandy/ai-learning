package main

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/Nickcandy/ai-learning/internal/courseenv"
	"github.com/cloudwego/eino-ext/components/model/openai"
	"github.com/cloudwego/eino/schema"
)

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}

func run() error {
	if err := courseenv.Load(".env"); err != nil {
		return err
	}
	apiKey, err := courseenv.Required("LLM_API_KEY")
	if err != nil {
		return err
	}
	modelName, err := courseenv.Required("LLM_MODEL")
	if err != nil {
		return err
	}
	zero := float32(0)
	model, err := openai.NewChatModel(context.Background(), &openai.ChatModelConfig{
		APIKey:      apiKey,
		BaseURL:     os.Getenv("LLM_BASE_URL"),
		Model:       modelName,
		Temperature: &zero,
		Timeout:     60 * time.Second,
	})
	if err != nil {
		return fmt.Errorf("create chat model: %w", err)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()
	answer, err := model.Generate(ctx, []*schema.Message{
		schema.SystemMessage("你是 AI Agent 面试官，使用中文简洁回答。"),
		schema.UserMessage("Eino 中 Message 的作用是什么？"),
	})
	if err != nil {
		return fmt.Errorf("generate answer: %w", err)
	}
	fmt.Println(answer.Content)
	if answer.ResponseMeta != nil {
		fmt.Printf("usage: %+v\n", answer.ResponseMeta.Usage)
	}
	return nil
}
