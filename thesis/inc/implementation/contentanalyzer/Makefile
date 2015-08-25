
DIA         = dia
INKSCAPE    = inkscape

all: \
    er_term_document_assignment.pdf \
    uml_vectors_simple.pdf \
    uml_document_vectors.pdf

clean: ; \
    rm ./*.pdf ./*.svg

root: ; \
    make -C ../../..

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


# uml_full
uml_full.svg: uml_full.dia ; \
    $(DIA) -e $@ -t svg $^

uml_full.pdf: uml_full.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

# uml_vectors
uml_vectors.svg: uml_vectors.dia ; \
    $(DIA) -e $@ -t svg $^

uml_vectors.pdf: uml_vectors.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

# uml_vectors_simple
uml_vectors_simple.svg: uml_vectors_simple.dia ; \
    $(DIA) -e $@ -t svg $^

uml_vectors_simple.pdf: uml_vectors_simple.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

# uml_term_document_product
uml_term_document_product.svg: uml_term_document_product.dia ; \
    $(DIA) -e $@ -t svg $^

uml_term_document_product.pdf: uml_term_document_product.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

# uml_document_vectors
uml_document_vectors.svg: uml_document_vectors.dia ; \
    $(DIA) -e $@ -t svg $^

uml_document_vectors.pdf: uml_document_vectors.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

# uml_vector_user
uml_vector_user.svg: uml_vector_user.dia ; \
    $(DIA) -e $@ -t svg $^

uml_vector_user.pdf: uml_vector_user.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

