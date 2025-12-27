# LibLogMCU 

## 简介

LiLogMCU 是纯头文件，提供了数个日志输出函数

定义了接受参数的宏，调用用户在 MCU 平台定义好的 `printf()` 函数，通过串口或其他接口打印日志

## Prerequisites

嵌入式平台一般没有内置的可用的 `printf()`，
若在嵌入式平台使用该库，需要用户事先重写 `fputc()` 即重定向 `printf()` 函数，

在 Keil MDK 中，需要首先勾选 `Use MicroLib` 之后写代码

```c 
#include "stdio.h"
#include "stdint.h"
#include "main.h"
#include "usart.h"

int fputc(int ch, FILE *f)
{
  // 在这里使用实际发送的接口重新定义发送功能
  // HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xffff);
  return ch;
}
int fgetc(FILE * f)
{
  // 在这里使用实际接受的接口重新定义接受功能
  uint8_t ch = 0;
  // HAL_UART_Receive(&huart1,&ch, 1, 0xffff);
  return ch;
}

```

## API Referrence

### LibLogMCU

头文件：`cc/neolux/libLogMCU/logger_mcu.h`

#### `LOG_LEVEL`

日志等级，高于该等级的日志不打印。可选：`LOG_LEVEL_ERROR`, `LOG_LEVEL_WARN`, `LOG_LEVEL_INFO`, `LOG_LEVEL_DEBUG`

#### `_LOG(level, fmt, ...)`

以 `level` 的日志等级输出日志 

- 参数：int level：日志等级，可选：`LOG_LEVEL_ERROR`, `LOG_LEVEL_WARN`, `LOG_LEVEL_INFO`, `LOG_LEVEL_DEBUG`
	   char \*b：格式字符串，要求同 `printf()`
	   ...：格式字符串所需数据，要求同 `printf()`
- 返回值：无

```
_LOG(LOG_LEVEL_INFO, "PID/P: %d", pid.p);
```

#### `LOG_E(fmt, ...)`

以错误等级输出日志。默认格式：`[level] [file:line] message`

- 参数：同 `printf()`
- 返回值：无

```
LOG_E("PID/P: %d", pid.p);
```

#### `LOG_W(fmt, ...)`

以警告等级输出日志。默认格式：`[level] [file:line] message`

- 参数：同 `printf()`
- 返回值：无

```
LOG_W("Get null from ir module: id=%02d!", irs[i].id);
```

#### `LOG_I(fmt, ...)`

以信息等级输出日志。默认格式：`[level] [file:line] message`

- 参数：同 `printf()`
- 返回值：无

```
LOG_I("All init done!");
```

#### `LOG_D(fmt, ...)`

以调试等级输出日志。默认格式：`[level] [file:line] message`

- 参数：同 `printf()`
- 返回值：无

```
LOG_D("L Motor Vel: %.03f", speed);
```
