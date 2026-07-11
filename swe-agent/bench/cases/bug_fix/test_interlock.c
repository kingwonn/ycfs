/* test_interlock.c — 联锁题判定测试(bench 判题用;埋 bug 前对参考实现全绿)。 */
#include <stdio.h>
#include "interlock.h"

static int passed = 0, failed = 0;
#define CHECK(c, n) do { if (c) passed++; else { failed++; printf("FAIL: %s\n", n); } } while (0)

static const ilk_cfg_t IC = {
    .rpm_derate = 60000u, .rpm_cutoff = 30000u, .sustain_ms = 300u,
    .cool_c = 45, .derate_cap_pm = 400u,
};

int main(void)
{
    ilk_ctx_t c;

    /* J1: 持续风量丧失 → CUTOFF 且指令归零 */
    ilk_init(&c);
    for (int i = 0; i < 20; i++) { ilk_step(&IC, &c, true, 0u, 90, 20); }
    CHECK(c.state == ILK_CUTOFF, "J1a sustained loss→CUTOFF");
    CHECK(ilk_apply(&IC, &c, 999u) == 0u, "J1b CUTOFF zeroes cmd");

    /* J2: 热态复位必须被拒(恢复需冷却确认)——本组抓「复位没查温度」的缺陷 */
    ilk_step(&IC, &c, true, 110000u, 90, 20);
    CHECK(c.state == ILK_CUTOFF, "J2 hot recovery refused");

    /* J3: 冷却 + 风量双满足才复位 */
    ilk_step(&IC, &c, true, 110000u, 40, 20);
    CHECK(c.state == ILK_OK, "J3 cool+airflow recovery ok");

    /* J4: 读数无效立即切断 */
    ilk_init(&c);
    ilk_step(&IC, &c, false, 110000u, 25, 20);
    CHECK(c.state == ILK_CUTOFF, "J4 invalid→CUTOFF");

    /* J5: DERATE 钳制 */
    ilk_init(&c);
    ilk_step(&IC, &c, true, 50000u, 60, 20);
    CHECK(ilk_apply(&IC, &c, 900u) == IC.derate_cap_pm, "J5 derate clamps");

    printf("RESULT: %d passed, %d failed\n", passed, failed);
    return failed == 0 ? 0 : 1;
}
