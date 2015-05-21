
DIA=dia

all: er_full.png
clean: ; \
    rm ./*.aux

root: ; \
    make -C ../..

er_full.png: er_full.dia ; \
    $(DIA) -e $@ -t png $^

