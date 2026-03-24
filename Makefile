.PHONY: all
MAKE               := make --no-print-directory
RUN 			   := uv run
VERSION            := v$(shell uv version --short)


# -- Testing ---
test:
	$(RUN) pytest $(ARGS) --no-cov

check:
	$(RUN) ruff check . $(ARGS)
	$(RUN) mypy . $(ARGS)

release:
	git tag $(VERSION)
	git push origin $(VERSION)

notes:
	# Thanks Will
	gh release create --generate-notes $(VERSION)
