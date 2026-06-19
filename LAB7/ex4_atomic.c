#include <stdio.h>
#include <pthread.h>

// Am adaugat "_Atomic" ca operatiunea sa fie thread-safe
_Atomic int counter = 0;

void* thread_routine(void* arg) {
    for(int i = 0; i < 100000; i++) {
        counter++;
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, thread_routine, NULL);
    pthread_create(&t2, NULL, thread_routine, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    
    printf("Valoare Atomic Corecta: %d (Asteptat: 200000)\n", counter);
    return 0;
}