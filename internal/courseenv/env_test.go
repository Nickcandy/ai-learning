package courseenv

import (
	"os"
	"path/filepath"
	"testing"
)

func TestLoad(t *testing.T) {
	t.Setenv("COURSE_EXISTING", "keep")
	path := filepath.Join(t.TempDir(), ".env")
	if err := os.WriteFile(path, []byte("COURSE_NEW=value\nCOURSE_EXISTING=replace\n"), 0o600); err != nil {
		t.Fatal(err)
	}
	if err := Load(path); err != nil {
		t.Fatal(err)
	}
	if got := os.Getenv("COURSE_NEW"); got != "value" {
		t.Fatalf("COURSE_NEW = %q", got)
	}
	if got := os.Getenv("COURSE_EXISTING"); got != "keep" {
		t.Fatalf("COURSE_EXISTING = %q", got)
	}
}
