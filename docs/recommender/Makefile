
TEX=pdflatex
DIA=dia
CPY=cp
RM=rm -f



all: recommender.pdf

clean: clean_childs ; \
    $(RM) *.aux *.log *.out recommender.pdf

clean_childs: ; \
    make -C ./inc/table_design clean

recommender.pdf: table_design code_design recommender.tex ; \
    $(TEX) recommender.tex

#table_design: er_information_retrieval_clothing.png
table_design: ; \
    make -C ./inc/table_design

code_design: ; \
    make -C ./inc/code_design

