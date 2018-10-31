CC = /usr/bin/gcc
CFLAGS = -Wall -Wextra -Wpedantic -O3

.PHONY: clean

libspx.so: sign.c api.h params.h
	$(CC) $(CFLAGS) -shared -o $@ -fPIC sign.c

clean:
	@rm libspx.so
