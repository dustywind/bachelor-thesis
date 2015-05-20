
DIA=dia

all: er_import_table.png

clean: ; \
    rm ./*.aux

root: ; \
    make -C ../..

er_import_table.png: er_import_table.dia ; \
    $(DIA) -e $@ -t png $^
