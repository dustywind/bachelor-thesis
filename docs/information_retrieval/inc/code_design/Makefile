
DIA=dia
INKSCAPE=inkscape

all: er_full.pdf er_vectors.pdf
clean: ; \
    rm ./*.aux er_full.png er_full.eps er_full.svg er_full.pdf

root: ; \
    make -C ../..

er_full.png: er_full.dia ; \
    $(DIA) -e $@ -t png $^

er_full.eps: er_full.dia ; \
    $(DIA) -e $@ -t eps $^

er_full.svg: er_full.dia ; \
    $(DIA) -e $@ -t svg $^

er_full.pdf: er_full.svg ; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@

er_vectors.svg: er_vectors.dia ; \
    $(DIA) -e $@ -t svg $^

er_vectors.pdf: er_vectors.svg; \
    $(INKSCAPE) -z -D --file=$^ --export-pdf=$@
    
