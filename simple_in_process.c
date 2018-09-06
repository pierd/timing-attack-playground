#include <stdio.h>
#include <string.h>
#include <time.h>
#include <mach/mach_time.h>

#define LENGTH 1024

char gKey[LENGTH + 1];
mach_timebase_info_data_t gInfo;

int vault(const char *key) {
    return strcmp(key, gKey) == 0;
}

uint64_t measure(const char *key) {
    uint64_t start = mach_absolute_time();
    vault(key);
    uint64_t stop = mach_absolute_time();
    return stop - start;
}

long min_measurement(unsigned int n, const char *key) {
    long min = 100000000;
    for (; n; n--) {
        long x = measure(key);
        if (x < min) {
            min = x;
        }
    }
    return min;
}

double avg_measurement(unsigned int n, const char *key) {
    long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += measure(key);
    }
    return (double)sum / n;
}

double to_nanos(double mach_units) {
    return mach_units * gInfo.numer / gInfo.denom;
}

int main(void) {
    if (mach_timebase_info(&gInfo) != KERN_SUCCESS) {
        return -1;
    }

    for (int i = 0; i < LENGTH; i++) {
        gKey[i] = '.';
    }
    gKey[LENGTH] = 0;

    char buffer[LENGTH + 1];
    for (int i = 0; i < LENGTH; i++) {
        strcpy(buffer, gKey);
        buffer[i] = 0;
        printf("%d %lf %lf\n", i, to_nanos(min_measurement(1000000, buffer)), to_nanos(avg_measurement(1000000, buffer)));
    }
    return 0;
}
