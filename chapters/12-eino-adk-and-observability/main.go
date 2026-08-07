package main

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"time"

	"github.com/Nickcandy/ai-learning/internal/courseenv"
	"github.com/cloudwego/eino-ext/components/model/openai"
	"github.com/cloudwego/eino/callbacks"
	"github.com/cloudwego/eino/components/tool"
	"github.com/cloudwego/eino/components/tool/utils"
	"github.com/cloudwego/eino/compose"
	flowagent "github.com/cloudwego/eino/flow/agent"
	"github.com/cloudwego/eino/flow/agent/react"
	"github.com/cloudwego/eino/schema"
)

type calculateInput struct {
	Left     float64 `json:"left" jsonschema:"required"`
	Operator string  `json:"operator" jsonschema:"required"`
	Right    float64 `json:"right" jsonschema:"required"`
}

func calculate(_ context.Context, input calculateInput) (float64, error) {
	switch input.Operator {
	case "add":
		return input.Left + input.Right, nil
	case "multiply":
		return input.Left * input.Right, nil
	case "divide":
		if input.Right == 0 {
			return 0, fmt.Errorf("divide by zero")
		}
		return input.Left / input.Right, nil
	default:
		return 0, fmt.Errorf("unsupported operator %q", input.Operator)
	}
}

func traceHandler() callbacks.Handler {
	return callbacks.NewHandlerBuilder().
		OnStartFn(func(ctx context.Context, info *callbacks.RunInfo, _ callbacks.CallbackInput) context.Context {
			if info != nil {
				slog.Info("component started", "name", info.Name, "type", info.Type)
			}
			return context.WithValue(ctx, startTimeKey{}, time.Now())
		}).
		OnEndFn(func(ctx context.Context, info *callbacks.RunInfo, _ callbacks.CallbackOutput) context.Context {
			startedAt, ok := ctx.Value(startTimeKey{}).(time.Time)
			if info != nil && ok {
				slog.Info("component finished", "name", info.Name, "elapsed", time.Since(startedAt))
			}
			return ctx
		}).
		OnErrorFn(func(ctx context.Context, info *callbacks.RunInfo, err error) context.Context {
			name := "unknown"
			if info != nil {
				name = info.Name
			}
			slog.Error("component failed", "name", name, "error", err)
			return ctx
		}).
		Build()
}

type startTimeKey struct{}

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
	model, err := openai.NewChatModel(context.Background(), &openai.ChatModelConfig{
		APIKey: apiKey, BaseURL: os.Getenv("LLM_BASE_URL"), Model: modelName, Timeout: 60 * time.Second,
	})
	if err != nil {
		return fmt.Errorf("create model: %w", err)
	}
	calculator, err := utils.InferTool("calculate", "执行 add、multiply 或 divide 运算", calculate)
	if err != nil {
		return fmt.Errorf("create tool: %w", err)
	}
	agent, err := react.NewAgent(context.Background(), &react.AgentConfig{
		ToolCallingModel: model,
		ToolsConfig:      compose.ToolsNodeConfig{Tools: []tool.BaseTool{calculator}},
		MaxStep:          8,
		MessageModifier: func(_ context.Context, input []*schema.Message) []*schema.Message {
			return append([]*schema.Message{schema.SystemMessage("计算必须使用 calculate 工具。")}, input...)
		},
	})
	if err != nil {
		return fmt.Errorf("create agent: %w", err)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()
	answer, err := agent.Generate(
		ctx,
		[]*schema.Message{schema.UserMessage("23 乘以 17 是多少？")},
		flowagent.WithComposeOptions(compose.WithCallbacks(traceHandler())),
	)
	if err != nil {
		return fmt.Errorf("run agent: %w", err)
	}
	fmt.Println(answer.Content)
	return nil
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
