OUTDIR = ../public_html

allpapers: all

all: car-26.pdf issac2000.pdf car-28.pdf rwca-02.pdf karlsruhe-02.pdf \
	linz-02.pdf clean

%.pdf:
	pdflatex $*
	pdflatex $*

clean:
	rm -rf *.bbl *.blg *.aux *.log *.dvi *.toc *~
