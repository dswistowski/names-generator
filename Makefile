docker: out/site.css
	 docker build . -t names-generator

out/site.css: ui/index.html src/site.css
	npx tailwindcss -i ./src/site.css -o ./ui/site.css

dev:
	npx tailwindcss -i ./src/site.css -o ./ui/site.css -w