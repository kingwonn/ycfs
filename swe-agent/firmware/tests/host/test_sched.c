/* test_sched.c — 裸机调度器 host 单测(gate host-unit-test 腿)。 */
#include <stdio.h>
#include "sched.h"

/* OSAL 接缝的 host 实现(测试注入) */
#include "osal.h"
static uint32_t s_now;
uint32_t osal_ticks(void) { return s_now; }

static int passed = 0, failed = 0;
#define CHECK(c, n) do { if (c) passed++; else { failed++; printf("FAIL: %s\n", n); } } while (0)

static int cnt_a, cnt_b, cnt_c;
static void fa(void) { cnt_a++; }
static void fb(void) { cnt_b++; }
static void fc(void) { cnt_c++; }

int main(void)
{
    sched_task_t tasks[] = {
        { fa,  1u, 0u, "a" },   /* 每 tick */
        { fb, 10u, 0u, "b" },   /* 每 10 tick */
        { fc,  0u, 0u, "c" },   /* period=0:每 tick */
    };
    sched_t s;
    sched_init(&s, tasks, 3, 0u);

    /* T1: 未到期不跑 */
    cnt_a = cnt_b = cnt_c = 0;
    int ran = sched_tick(&s, 1u);
    CHECK(cnt_b == 0, "T1 period=10 在 tick1 不跑");
    /* T2: 每 tick 任务与 period=0 任务都跑 */
    CHECK(cnt_a == 1 && cnt_c == 1 && ran == 2, "T2 每tick任务跑且计数=2");

    /* T3: 恰到期跑一次 */
    for (uint32_t t = 2; t <= 10; t++) sched_tick(&s, t);
    CHECK(cnt_b == 1, "T3 period=10 在 tick10 恰跑一次");

    /* T4: 两任务不同周期正确交错 */
    CHECK(cnt_a == 10, "T4 每tick任务跑满 10 次");

    /* T5: 无过载时 overruns=0 */
    CHECK(s.overruns == 0u, "T5 正常节拍无过载");

    /* T6: 独立调度器,跳 3.5 个周期 → 过载计数 +1,但只补跑一次(防雪崩) */
    sched_task_t ot[] = { { fb, 10u, 0u, "ob" } };
    sched_t s3; sched_init(&s3, ot, 1, 10u);
    int b_before = cnt_b;
    sched_tick(&s3, 45u);
    CHECK(s3.overruns == 1u, "T6a 过载被计数");
    CHECK(cnt_b == b_before + 1, "T6b 过载只补跑一次不追积压");

    /* T7: 过载后重同步,下个周期正常 */
    sched_tick(&s3, 55u);
    CHECK(s3.overruns == 1u && cnt_b == b_before + 2, "T7 重同步后按新相位运行且不再计过载");

    /* T8: tick 回绕安全(无符号差) */
    sched_task_t w[] = { { fa, 10u, 0u, "w" } };
    sched_t s2; sched_init(&s2, w, 1, 0xFFFFFFF8u);
    cnt_a = 0;
    sched_tick(&s2, 0x00000002u);   /* 跨回绕 elapsed=10 */
    CHECK(cnt_a == 1, "T8 计数回绕处任务照常到期");

    printf("RESULT: %d passed, %d failed\n", passed, failed);
    return failed == 0 ? 0 : 1;
}
