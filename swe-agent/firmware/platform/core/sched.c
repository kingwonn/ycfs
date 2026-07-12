#include "sched.h"

void sched_init(sched_t *s, sched_task_t *tasks, int n, uint32_t now)
{
    s->tasks = tasks;
    s->n = n;
    s->overruns = 0u;
    for (int i = 0; i < n; i++) {
        tasks[i].last_run = now;
    }
}

int sched_tick(sched_t *s, uint32_t now)
{
    int ran = 0;
    for (int i = 0; i < s->n; i++) {
        sched_task_t *t = &s->tasks[i];
        uint32_t elapsed = now - t->last_run;   /* 无符号回绕安全 */
        if ((t->period_ticks == 0u) || (elapsed >= t->period_ticks)) {
            if ((t->period_ticks != 0u) && (elapsed >= (2u * t->period_ticks))) {
                s->overruns++;                  /* 过载:错过≥1个整周期 */
            }
            t->fn();
            ran++;
            /* 重同步到 now(而非 last+period):过载后不追补积压,防雪崩 */
            t->last_run = now;
        }
    }
    return ran;
}
