
PDFLATEX        = pdflatex
BIBTEX          = bibtex
GLOSSARY        = makeglossaries
INDEX           = makeindex
RM              = rm -f
MKDIR           = mkdir -p
CP              = cp -f
OUTDIR          = ./out
PROJECTNAME     = thesis
OUTPUTFILENAME  = $(PROJECTNAME).pdf
 TORM           = *.aux *.log *.toc *.out *.pdf *.run.xml *.bbl *.bcf *.blg *-blx.bib *.xdy *.glo *.lof *.lol *.lot

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

all: dependencies online copy;

dependencies: ; \
    make -C ./inc/implementation

copy: ; \
    $(MKDIR) $(OUTDIR) && \
    $(CP) $(OUTPUTFILENAME) $(OUTDIR)

online: ; \
    $(PDFLATEX) -jobname=$(PROJECTNAME) "$(VARS)\input{$(PROJECTNAME).tex}"

print: ; \
    $(PDFLATEX) -jobname=$(PROJECTNAME) "$(PRINT)$(VARS)\input{$(PROJECTNAME).tex}"

bib: ; \
    $(BIBTEX) $(PROJECTNAME)

glo: ; \
    $(GLOSSARY) $(PROJECTNAME).glo

idx: ; \
    $(INDEX) $(PROJECTNAME).idx

clean: ; \
    $(RM) $(TORM)
