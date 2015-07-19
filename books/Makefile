

ENCRYPTEDFILE   = books.tar.gz.enc


COMPRESS        = tar c `ls . | grep -v $(ENCRYPTEDFILE) | grep -v Makefile` | gzip 
DECOMPRESS      = gzip -d | tar xv
ENCRYPT         = openssl enc -aes-256-cbc -e
DECRYPT         = openssl aes-256-cbc -d -in



unpack: books.tar.gz.enc ; \
    $(DECRYPT) $(ENCRYPTEDFILE) | $(DECOMPRESS)

pack: ; \
    $(COMPRESS) | $(ENCRYPT) > $(ENCRYPTEDFILE)


