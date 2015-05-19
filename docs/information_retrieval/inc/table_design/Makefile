
DIA=dia

all: er_information_retrieval_clothing.png

clean: ; \
    rm ./*.aux

root: ; \
    make -C ../..

er_information_retrieval_clothing.png: er_information_retrieval_clothing.dia ; \
    $(DIA) -e $@ -t png $^
