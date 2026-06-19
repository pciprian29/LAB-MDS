#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char* name;
    int* grades;
    int   count;
} Student;

Student* new_student(const char* name, int grades[], int n) {
    Student* s = malloc(sizeof(Student));
    // Reparat: am adaugat + 1 pentru caracterul nul '\0' de la finalul stringului
    s->name = malloc(strlen(name) + 1);  
    strcpy(s->name, name);
    s->grades = malloc(n * sizeof(int));
    memcpy(s->grades, grades, n * sizeof(int));
    s->count = n;
    return s;
}

float average(Student* s) {
    int sum = 0;
    // Reparat: conditia de oprire este i < s->count, altfel iesim din memorie
    for (int i = 0; i < s->count; i++) {  
        sum += s->grades[i];
    }
    return (float)sum / s->count;
}

void free_student(Student* s) {
    free(s->name);
    // Reparat: eliberam array-ul de note inainte sa eliberam intregul student (leak memory fix)
    free(s->grades);
    free(s);
}

int main() {
    int grades[] = {85, 90, 78, 92};
    Student* alice = new_student("Alice", grades, 4);
    printf("%s: avg = %.1f\n", alice->name, average(alice));
    free_student(alice);
    return 0;
}