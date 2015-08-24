
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
VARS            = \def\dustAuthor{Dusty Wind} \
                    \def\dustStreet{Street} \
                    \def\dustNumber{num} \
                    \def\dustPlz{PLZ} \
                    \def\dustCityPartOne{city} \
                    \def\dustCityPartTwo{city} \
                    \def\dustMatrnr{666} \
                    \def\dustCourse{something interesting} \
                    \def\dustProf{prof.} \
                    \def\dustTutor{tutor} \
                    \def\dustStartDay{some day} \
                    \def\dustEndDay{another day}


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
