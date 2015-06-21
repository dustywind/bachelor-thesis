
PDFLATEX    = pdflatex
BIBTEX      = bibtex
RM          = rm -f

PROJECTNAME = interimreport


.PHONY: all bib count clean copy

all: online;

interimreport: ; \
    $(PDFLATEX) -jobname=$@ "\input{$@.tex}"

print: ; \
    $(PDFLATEX) -jobname=$(PROJECTNAME) "\def\PRINT{}\input{interimsreport.tex}"

bib: ; \
    $(BIBTEX) interimreport

clean: ; \
    $(RM) *.aux *.log *.toc *.out *.pdf *.run.xml *.bbl *.bcf *.blg *-blx.bib


