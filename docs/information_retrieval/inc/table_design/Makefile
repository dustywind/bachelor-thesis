
DIA=dia

all: er_import_table.png er_term_document_assignment.png 
clean: ; \
    rm ./*.aux

root: ; \
    make -C ../..

er_import_table.png: er_import_table.dia ; \
    $(DIA) -e $@ -t png $^

er_term_document_assignment.png: er_term_document_assignment.dia ; \
    $(DIA) -e $@ -t png $^


