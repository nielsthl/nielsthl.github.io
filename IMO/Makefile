COMPILER = qadil/qadil.py
CHAPTERDIR = .
GENTOC = qadil/gentoc.py
GENLABELS = qadil/genlbls.py

all: book labels toc

book: $(CHAPTERDIR)/index.html $(CHAPTERDIR)/intro.html $(CHAPTERDIR)/lineqs.html $(CHAPTERDIR)/matrices.html  $(CHAPTERDIR)/whatisopt.html  $(CHAPTERDIR)/euclidean.html

#book: $(CHAPTERDIR)/index.html $(CHAPTERDIR)/whatisopt.html $(CHAPTERDIR)/appendixA.html

labels:
	python3 $(GENLABELS) $(CHAPTERDIR) 

toc:
	python3 $(GENTOC) $(CHAPTERDIR)

%.html: %.tex
	python3 $(COMPILER) $<

clean:
	rm -f $(CHAPTERDIR)/*.html $(CHAPTERDIR)/*.toc $(CHAPTERDIR)/*.lbl $(CHAPTERDIR)/*~

zip:
	zip -r IMO.zip *.html img/ js/ css/
 
