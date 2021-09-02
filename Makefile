clean:
	@rm -rf build dist .eggs *.egg-info
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +

black: clean
	@isort --profile black setup.py salon/
	@black setup.py salon/
	
.PHONY: docs

docs:
	@pylode -i SALON.owl -o ./docs/index.html
	@sed -i '' 's,href="http://www.ontologies.khaos.uma.es/salon/,target="_parent" href="https://ontologies.khaos.uma.es/salon/,g' ./docs/index.html
