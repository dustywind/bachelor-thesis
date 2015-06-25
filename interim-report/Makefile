
PDFLATEX    = pdflatex
BIBTEX      = bibtex
RM          = rm -f

PROJECTNAME = interimreport
PRINT       = \def\PRINT{}
VARS        = \def\myAuthor{Dusty Wind} \
                \def\myStreet{Street} \
                \def\myNumber{num} \
                \def\myPlz{PLZ} \
                \def\myCity{city} \
                \def\myMatrnr{666} \
                \def\myCourse{something interesting} \
                \def\myProf{prof.} \
                \def\myTutor{tutor}


.PHONY: all bib count clean copy

all: online;

online: ; \
    $(PDFLATEX) -jobname=$(PROJECTNAME) "$(VARS)\input{$(PROJECTNAME).tex}"

print: ; \
    $(PDFLATEX) -jobname=$(PROJECTNAME) "$(PRINT)$(VARS)\input{$(PROJECTNAME).tex}"

bib: ; \
    $(BIBTEX) interimreport

clean: ; \
    $(RM) *.aux *.log *.toc *.out *.pdf *.run.xml *.bbl *.bcf *.blg *-blx.bib


