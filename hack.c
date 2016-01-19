#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int puts(const char *s) {

    const char *my_puts = "My puts \n";
    size_t my_puts_count = strlen(my_puts);
    size_t s_count;

    write(0, my_puts, my_puts_count);


    s_count = strlen(s);

    write(0, s, s_count);
}
