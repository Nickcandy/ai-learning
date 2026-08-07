package main

import (
	"context"
	"testing"
)

func TestCalculateRejectsDivisionByZero(t *testing.T) {
	_, err := calculate(context.Background(), calculateInput{Left: 1, Operator: "divide", Right: 0})
	if err == nil {
		t.Fatal("expected division by zero error")
	}
}
