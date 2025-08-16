.PHONY: clean dry-run

clean:
	@echo "Deleting all migrations and __pycache__ folders (excluding .venv)..."
	@find . -path './.venv' -prune -o \( -type d \( -name 'migrations' -o -name '__pycache__' \) \) -print | while read dir; do \
		echo "Deleted from: $$(basename $$(dirname "$$dir"))"; \
		rm -rf "$$dir"; \
	done

dry-run:
	@echo "Dry-run: showing all migrations and __pycache__ folders (excluding .venv)..."
	@find . -path './.venv' -prune -o \( -type d \( -name 'migrations' -o -name '__pycache__' \) \) -print | while read dir; do \
		echo "Would delete from: $$(basename $$(dirname "$$dir"))"; \
	done
