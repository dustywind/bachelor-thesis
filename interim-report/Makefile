
PDFLATEX    = pdflatex
BIBTEX      = bibtex
RM          = rm -f


.PHONY: all bib count clean copy

all: pdf;

pdf: ; \
    $(PDFLATEX) interimreport.tex

bib: ; \
    $(BIBTEX) interimreport

clean: ; \
    $(RM) *.aux *.log *.toc *.out *.pdf *.run.xml *.bbl *.bcf *.blg *-blx.bib


