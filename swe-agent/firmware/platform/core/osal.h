/*
 * osal.h — 薄 OSAL 接缝(D-006:裸机优先,RTOS 后议)。
 * 裸机形态下这些是空操作/直通;未来上 FreeRTOS/Zephyr 时只换本文件的实现,
 * platform 与 products 层零改动。接口只加不减。
 */
#ifndef OSAL_H
#define OSAL_H

#include <stdint.h>

/* 裸机:单核无抢占应用任务,临界区留空;上 RTOS/使能中断共享数据时换实现 */
#define OSAL_CRITICAL_ENTER() do { } while (0)
#define OSAL_CRITICAL_EXIT()  do { } while (0)

/* 系统节拍(裸机=SysTick 计数;host 单测=测试注入) */
uint32_t osal_ticks(void);

#endif /* OSAL_H */
