package main

import (
	"context"
	"fmt"
	"os"
	"sort"
	"strings"

	"github.com/cloudwego/eino/components/retriever"
	"github.com/cloudwego/eino/compose"
	"github.com/cloudwego/eino/schema"
)

type keywordRetriever struct {
	documents []*schema.Document
}

func (r *keywordRetriever) Retrieve(ctx context.Context, query string, _ ...retriever.Option) ([]*schema.Document, error) {
	if err := ctx.Err(); err != nil {
		return nil, fmt.Errorf("retrieve canceled: %w", err)
	}
	terms := strings.Fields(strings.ToLower(query))
	if len(terms) == 0 {
		return nil, fmt.Errorf("query is empty")
	}
	type match struct {
		document *schema.Document
		score    int
	}
	matches := make([]match, 0, len(r.documents))
	for _, document := range r.documents {
		content := strings.ToLower(document.Content)
		score := 0
		for _, term := range terms {
			if strings.Contains(content, term) {
				score++
			}
		}
		if score > 0 {
			matches = append(matches, match{document: document, score: score})
		}
	}
	sort.SliceStable(matches, func(i, j int) bool { return matches[i].score > matches[j].score })
	result := make([]*schema.Document, 0, len(matches))
	for _, item := range matches {
		document := *item.document
		result = append(result, document.WithScore(float64(item.score)))
	}
	return result, nil
}

func formatDocuments(_ context.Context, documents []*schema.Document) (string, error) {
	if len(documents) == 0 {
		return "资料不足，无法回答。", nil
	}
	var builder strings.Builder
	for _, document := range documents {
		fmt.Fprintf(&builder, "[%s] %s\n", document.ID, document.Content)
	}
	return builder.String(), nil
}

func buildGraph(ctx context.Context, r retriever.Retriever) (compose.Runnable[string, string], error) {
	graph := compose.NewGraph[string, string]()
	if err := graph.AddRetrieverNode("retrieve", r); err != nil {
		return nil, fmt.Errorf("add retriever: %w", err)
	}
	if err := graph.AddLambdaNode("format", compose.InvokableLambda(formatDocuments)); err != nil {
		return nil, fmt.Errorf("add formatter: %w", err)
	}
	if err := graph.AddEdge(compose.START, "retrieve"); err != nil {
		return nil, fmt.Errorf("connect start: %w", err)
	}
	if err := graph.AddEdge("retrieve", "format"); err != nil {
		return nil, fmt.Errorf("connect retriever: %w", err)
	}
	if err := graph.AddEdge("format", compose.END); err != nil {
		return nil, fmt.Errorf("connect end: %w", err)
	}
	return graph.Compile(ctx, compose.WithGraphName("rag-retrieval"))
}

func run() error {
	ctx := context.Background()
	r := &keywordRetriever{documents: []*schema.Document{
		{ID: "chunk-01", Content: "tool calling lets a model request application tools"},
		{ID: "chunk-02", Content: "checkpoint stores graph state for later resume"},
	}}
	graph, err := buildGraph(ctx, r)
	if err != nil {
		return err
	}
	result, err := graph.Invoke(ctx, "tool calling")
	if err != nil {
		return fmt.Errorf("invoke graph: %w", err)
	}
	fmt.Print(result)
	return nil
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
