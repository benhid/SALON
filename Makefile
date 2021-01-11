.PHONY: docs

docs:
	@pylode -i SALON.owl -o ./docs/index.html
	@sed -i '' 's,href="http://www.ontologies.khaos.uma.es/salon/,target="_parent" href="https://ontologies.khaos.uma.es/salon/,g' ./docs/index.html
