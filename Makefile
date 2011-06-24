all: trup16.tar.gz

CURRENT=reviver.py
LIBS=comb.py eval.py game.py target_finder.py README

trup16.tar.gz: install $(CURRENT) $(LIBS)
	cp $(CURRENT) run
	tar czf trup16.tar.gz install run $(LIBS)

clean:
	rm -f trup16.tar.gz run
