OUTDIR = ../public_html

allpapers: all

all: linz-06.pdf clean

%.pdf:
	pdflatex $*
	pdflatex $*

clean:
	rm -rf *.bbl *.blg *.aux *.log *.dvi *.toc *~
