#ifndef __CC_NEOLUX_LIBLOGMCU_LOGGER_MCU_H
#define __CC_NEOLUX_LIBLOGMCU_LOGGER_MCU_H

#include "stdio.h"

#define LOG_LEVEL_NONE			0
#define LOG_LEVEL_ERROR   1
#define LOG_LEVEL_WARN    2
#define LOG_LEVEL_INFO    3
#define LOG_LEVEL_DEBUG   4

#define LOG_LEVEL LOG_LEVEL_INFO

#define _LOG(level, fmt, ...) do { \
    if (level <= LOG_LEVEL) { \
        const char* lvl_str = (level == LOG_LEVEL_ERROR) ? "ERROR" : \
                              (level == LOG_LEVEL_WARN)  ? "WARN"  : \
                              (level == LOG_LEVEL_INFO)  ? "INFO"  : "DEBUG"; \
        printf("[%s] [%s:%d] " fmt "\r\n", lvl_str, __FILE__, __LINE__, ##__VA_ARGS__); \
    } \
} while (0)

#define LOG_E(fmt, ...) _LOG(LOG_LEVEL_ERROR, fmt, ##__VA_ARGS__)
#define LOG_W(fmt, ...) _LOG(LOG_LEVEL_WARN,  fmt, ##__VA_ARGS__)
#define LOG_I(fmt, ...) _LOG(LOG_LEVEL_INFO,  fmt, ##__VA_ARGS__)
#define LOG_D(fmt, ...) _LOG(LOG_LEVEL_DEBUG, fmt, ##__VA_ARGS__)

#endif