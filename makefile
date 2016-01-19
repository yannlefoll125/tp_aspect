all: hack hello

hack: hack.c
	gcc -fPIC -shared -o hack.so hack.c

hello: hello.c
	gcc -o hello hello.c


