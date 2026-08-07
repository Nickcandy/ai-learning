package main

import (
	"context"
	"strings"
	"testing"

	"github.com/cloudwego/eino/schema"
)

func TestGraphRetrievesAndFormatsEvidence(t *testing.T) {
	r := &keywordRetriever{documents: []*schema.Document{
		{ID: "relevant", Content: "tool calling uses an application tool"},
		{ID: "other", Content: "memory stores conversation state"},
	}}
	graph, err := buildGraph(context.Background(), r)
	if err != nil {
		t.Fatal(err)
	}
	result, err := graph.Invoke(context.Background(), "tool calling")
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(result, "[relevant]") || strings.Contains(result, "[other]") {
		t.Fatalf("unexpected result: %s", result)
	}
}
