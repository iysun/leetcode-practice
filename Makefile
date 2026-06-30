ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ID   := $(word 2,$(MAKECMDGOALS))
  RUN_LANG := $(word 3,$(MAKECMDGOALS))
endif

ifeq (gen,$(firstword $(MAKECMDGOALS)))
  GEN_ID   := $(word 2,$(MAKECMDGOALS))
  GEN_LANG := $(word 3,$(MAKECMDGOALS))
endif

# FORCE=1 to overwrite existing files: make gen 121 FORCE=1
FORCE ?= 0

.PHONY: help run gen

# Absorb extra arguments so make doesn't treat them as targets
%:
	@:

help:
	@echo "Usage:"
	@echo "  make gen <id> [go|py] [FORCE=1]  Generate problem template"
	@echo "  make run <id> [go|py]             Run solution file(s)"
	@echo ""
	@echo "Examples:"
	@echo "  make gen 121                      Generate Go + Python for problem 121"
	@echo "  make gen 121 go                   Go only"
	@echo "  make gen 121 py FORCE=1           Python only, overwrite existing"
	@echo "  make run 121                      Run Go + Python for problem 121"
	@echo "  make run 121 go                   Go only"
	@echo "  make run 121 py                   Python only"

run:
	@if [ -z "$(RUN_ID)" ]; then \
		echo "Usage: make run <problem-id> [go|py]"; \
		echo "  make run 0121        # run both languages"; \
		echo "  make run 0121 go     # Go only"; \
		echo "  make run 0121 py     # Python only"; \
		exit 1; \
	fi; \
	lang="$(RUN_LANG)"; \
	if [ -n "$$lang" ] && [ "$$lang" != "go" ] && [ "$$lang" != "py" ]; then \
		echo "Error: unsupported language '$$lang', use 'go' or 'py'"; \
		exit 1; \
	fi; \
	id=$$(printf '%04d' "$$((10#$(RUN_ID)))"); \
	go_file=$$(ls solutions/go/$${id}_*.go 2>/dev/null | head -1); \
	py_file=$$(ls solutions/py/$${id}_*.py 2>/dev/null | head -1); \
	if [ -z "$$go_file" ] && [ -z "$$py_file" ]; then \
		echo "Error: no solution files found for problem $${id}"; \
		exit 1; \
	fi; \
	if [ "$$lang" != "py" ] && [ -n "$$go_file" ]; then \
		echo "==> Go: $$go_file"; \
		go run "$$go_file"; \
	fi; \
	if [ "$$lang" != "go" ] && [ -n "$$py_file" ]; then \
		echo "==> Python: $$py_file"; \
		python "$$py_file"; \
	fi

gen:
	@if [ -z "$(GEN_ID)" ]; then \
		echo "Usage: make gen <problem-id> [go|py] [FORCE=1]"; \
		echo "  make gen 121           # generate both languages"; \
		echo "  make gen 121 go        # Go only"; \
		echo "  make gen 121 py        # Python only"; \
		echo "  make gen 121 FORCE=1   # overwrite existing files"; \
		exit 1; \
	fi; \
	lang="$(GEN_LANG)"; \
	if [ -n "$$lang" ] && [ "$$lang" != "go" ] && [ "$$lang" != "py" ]; then \
		echo "Error: unsupported language '$$lang', use 'go' or 'py'"; \
		exit 1; \
	fi; \
	cmd="python .claude/skills/leetcode-generate-problem/scripts/run_generate_problem.py $(GEN_ID)"; \
	[ -n "$$lang" ] && cmd="$$cmd --lang $$lang"; \
	[ "$(FORCE)" = "1" ] && cmd="$$cmd --force"; \
	$$cmd
