/*
 * sched.h — 裸机主循环任务表调度器(D-006)。
 * 纯逻辑、无硬件依赖,host 单测覆盖(gate host-unit-test 腿)。
 * 用法:products 层注册任务表(周期以 tick 计),主循环里喂 sched_tick(now)。
 * FOC 电流环不走这里——它住定时器/ADC ISR(MCSDK 形态);这里只管应用层节拍
 * (速度环 ~1kHz / 温度环 20–100Hz / HMI ~10Hz)。
 */
#ifndef SCHED_H
#define SCHED_H

#include <stdint.h>

typedef void (*sched_fn_t)(void);

typedef struct {
    sched_fn_t  fn;
    uint32_t    period_ticks;   /* 0 = 每 tick 都跑 */
    uint32_t    last_run;       /* 内部状态 */
    const char *name;
} sched_task_t;

typedef struct {
    sched_task_t *tasks;
    int           n;
    uint32_t      overruns;     /* 错过 ≥2 个周期的次数(过载观测,审计可读) */
} sched_t;

void sched_init(sched_t *s, sched_task_t *tasks, int n, uint32_t now);
/* 跑完当前 tick 所有到期任务;返回本次运行的任务数 */
int  sched_tick(sched_t *s, uint32_t now);

#endif /* SCHED_H */
