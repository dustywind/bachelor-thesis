
PDFLATEX        = pdflatex
BIBTEX          = bibtex
RM              = rm -f
MKDIR           = mkdir -p
CP              = cp -f
OUTDIR          = ./out
PROJECTNAME     = thesis
OUTPUTFILENAME  = $(PROJECTNAME).pdf

PRINT           = \def\PRINT{}
VARS            = \def\myAuthor{Dusty Wind} \
                    \def\myStreet{Street} \
                    \def\myNumber{num} \
                    \def\myPlz{PLZ} \
                    \def\myCityPartOne{city} \
                    \def\myCityPartTwo{city} \
                    \def\myMatrnr{666} \
                    \def\myCourse{something interesting} \
                    \def\myProf{prof.} \
                    \def\myTutor{tutor}


.PHONY: all bib count clean copy

all: online copy;

copy: ; \
    $(MKDIR) $(OUTDIR) && \
    $(CP) $(OUTPUTFILENAME) $(OUTDIR)

online: ; \
    $(PDFLATEX) -jobname=$(PROJECTNAME) "$(VARS)\input{$(PROJECTNAME).tex}"

print: ; \
    $(PDFLATEX) -jobname=$(PROJECTNAME) "$(PRINT)$(VARS)\input{$(PROJECTNAME).tex}"

bib: ; \
    $(BIBTEX) $(PROJECTNAME)

clean: ; \
    $(RM) *.aux *.log *.toc *.out *.pdf *.run.xml *.bbl *.bcf *.blg *-blx.bib *.xdy *.glo *.lof


