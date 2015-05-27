
TEX=pdflatex
DIA=dia
CPY=cp
RM=rm -f



all: ir.pdf

clean: clean_childs ; \
    $(RM) *.aux *.log *.out ir.pdf

clean_childs: ; \
    make -C ./inc/table_design clean

ir.pdf: table_design code_design ir_info.tex ; \
    $(TEX) ir_info.tex

#table_design: er_information_retrieval_clothing.png
table_design: ; \
    make -C ./inc/table_design

code_design: ; \
    make -C ./inc/code_design

