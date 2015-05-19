
TEX=pdflatex
DIA=dia
CPY=cp
RM=rm -f



all: ir.pdf

clean: ; \
    $(RM) *.aux *.log *.out ir.pdf

ir.pdf: table_design ir_info.tex ; \
    $(TEX) ir_info.tex

#table_design: er_information_retrieval_clothing.png
table_design: ; \
    make -C ./inc/table_design

