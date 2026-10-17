run:
	bootdev run
sub:
	yes | bootdev run -s
main:
	./main.sh
test:
	./test.sh
serve:
	python3 -m http.server 8888 -d public
