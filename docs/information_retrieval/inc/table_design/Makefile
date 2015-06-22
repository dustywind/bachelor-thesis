
DIA=dia
INKSCAPE=inkscape

all: er_import_table.pdf er_term_document_assignment.pdf er_user_table.pdf
clean: ; \
    rm ./*.aux

root: ; \
    make -C ../..

er_import_table.png: er_import_table.dia ; \
    $(DIA) -e $@ -t png $^

er_import_table.svg: er_import_table.dia ; \
    $(DIA) -e $@ -t svg $^

er_import_table.pdf: er_import_table.svg ; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

er_term_document_assignment.png: er_term_document_assignment.dia ; \
    $(DIA) -e $@ -t png $^

er_term_document_assignment.svg: er_term_document_assignment.dia ; \
    $(DIA) -e $@ -t svg $^

er_term_document_assignment.pdf: er_term_document_assignment.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

er_user_table.svg: er_user_table.dia ; \
    $(DIA) -e $@ -t svg $^

er_user_table.pdf: er_user_table.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

