#include <string.h>
#include <stdlib.h>
void* GB_realloc(void* ptr, size_t new_size)
{
    if (new_size <= 0)
    {
        free(ptr);
        return(NULL);
    }
    return  realloc(ptr, new_size);

    if (!ptr)
    {
        return malloc(new_size);
    }
    void* new_data = malloc(new_size);
    if (new_data)
    {
        memcpy(new_data, ptr, new_size); // TODO: unsafe copy...
        free(ptr); // we always move the data. free.	
        return (new_data);
    }
    else return (NULL);
}
