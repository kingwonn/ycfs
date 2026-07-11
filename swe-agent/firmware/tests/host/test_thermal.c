/* test_thermal.c — 温控 PI+前馈 与 电机-加热联锁 host 单测(gate host-unit-test 腿)。 */
#include <math.h>
#include <stdio.h>
#include "interlock.h"
#include "thermal_pi.h"

static int passed = 0, failed = 0;
#define CHECK(c, n) do { if (c) passed++; else { failed++; printf("FAIL: %s\n", n); } } while (0)

/* PROVENANCE: PLACEHOLDER(测试参数,真机标定前不代表产品值) */
static const thermal_cfg_t TC = {
    .kp_pm_per_c = 30.0f, .ki_pm_per_c_s = 8.0f, .ff_pm_per_level = 60.0f,
    .out_max_pm = 1000.0f, .hard_limit_c = 115,
};
static const ilk_cfg_t IC = {
    .rpm_derate = 60000u, .rpm_cutoff = 30000u, .sustain_ms = 300u,
    .cool_c = 45, .derate_cap_pm = 400u,
};

int main(void)
{
    thermal_ctx_t tc;
    ilk_ctx_t ic;

    /* ── 温控 PI ── */
    /* T1: 冷启动大误差 → 输出饱和到上限 */
    thermal_init(&tc);
    float out = thermal_step(&TC, &tc, 80, 25, 0, 20);
    CHECK(out == 1000.0f, "T1 大误差输出饱和上限");

    /* T2: 风量前馈:同误差,档位差 2 档 → 输出差 2×ff */
    thermal_ctx_t a, b; thermal_init(&a); thermal_init(&b);
    float o0 = thermal_step(&TC, &a, 60, 55, 0, 20);
    float o2 = thermal_step(&TC, &b, 60, 55, 2, 20);
    CHECK(fabsf((o2 - o0) - 2.0f * TC.ff_pm_per_level) < 0.01f, "T2 前馈按档位线性叠加");

    /* T3: 硬顶:测温≥hard_limit → 强制 0 */
    thermal_init(&tc);
    CHECK(thermal_step(&TC, &tc, 80, 115, 3, 20) == 0.0f, "T3 硬顶断热");

    /* T4: 抗饱和:长期饱和后误差反向,输出一步内脱离上限 */
    thermal_init(&tc);
    for (int i = 0; i < 500; i++) { (void)thermal_step(&TC, &tc, 80, 25, 0, 20); }
    out = thermal_step(&TC, &tc, 80, 95, 0, 20);   /* 误差反向 */
    CHECK(out < 1000.0f, "T4 条件积分抗饱和:反向后立即退出饱和");

    /* T5: 一阶炉温仿真收敛:200 步(20s)内到设定 ±3°C 且过冲 ≤5°C */
    thermal_init(&tc);
    float temp = 25.0f, peak = 25.0f;
    for (int i = 0; i < 1000; i++) {
        out = thermal_step(&TC, &tc, 80, (int16_t)temp, 1, 100);
        temp += (out * 0.003f - (temp - 25.0f) * 0.05f) * 1.0f;  /* 简化一阶植物 */
        if (temp > peak) { peak = temp; }
    }
    CHECK(temp > 77.0f && temp < 83.0f, "T5a 仿真收敛到设定±3°C");
    CHECK(peak <= 85.0f, "T5b 过冲 ≤5°C(伤发线防护的缩影)");

    /* ── 联锁 ── */
    /* T6: 正常风量 → OK,指令原样通过 */
    ilk_init(&ic);
    CHECK(ilk_step(&IC, &ic, true, 100000u, 60, 20) == ILK_OK, "T6a 正常风量 OK");
    CHECK(ilk_apply(&IC, &ic, 900u) == 900u, "T6b OK 态指令直通");

    /* T7: 风量偏低 → DERATE,指令被钳到上限 */
    ilk_step(&IC, &ic, true, 50000u, 60, 20);
    CHECK(ic.state == ILK_DERATE, "T7a 低风量降档");
    CHECK(ilk_apply(&IC, &ic, 900u) == IC.derate_cap_pm, "T7b DERATE 钳制");

    /* T8: 风量丧失持续 300ms → CUTOFF;闩锁 */
    ilk_init(&ic);
    for (int i = 0; i < 15; i++) { ilk_step(&IC, &ic, true, 10000u, 90, 20); }
    CHECK(ic.state == ILK_CUTOFF, "T8a 持续低风量切断");
    CHECK(ilk_apply(&IC, &ic, 900u) == 0u, "T8b CUTOFF 态归零");

    /* T9: 间歇低风量(每次<300ms,中间恢复)→ 不误切 */
    ilk_init(&ic);
    for (int r = 0; r < 3; r++) {
        for (int i = 0; i < 10; i++) { ilk_step(&IC, &ic, true, 10000u, 60, 20); }
        ilk_step(&IC, &ic, true, 100000u, 60, 20);
    }
    CHECK(ic.state != ILK_CUTOFF, "T9 间歇低风量不误切");

    /* T10: 恢复需双条件:风量回来但仍烫 → 保持 CUTOFF;冷却后才复位 */
    ilk_init(&ic);
    for (int i = 0; i < 15; i++) { ilk_step(&IC, &ic, true, 10000u, 90, 20); }
    ilk_step(&IC, &ic, true, 100000u, 90, 20);
    CHECK(ic.state == ILK_CUTOFF, "T10a 热态复位被拒(恢复需冷却确认)");
    ilk_step(&IC, &ic, true, 100000u, 40, 20);
    CHECK(ic.state == ILK_OK, "T10b 冷却+风量双满足才复位");

    /* T11: 读数无效 → 立即 CUTOFF(最危险假设) */
    ilk_init(&ic);
    ilk_step(&IC, &ic, false, 100000u, 25, 20);
    CHECK(ic.state == ILK_CUTOFF, "T11 无效读数立即切断");

    printf("RESULT: %d passed, %d failed\n", passed, failed);
    return failed == 0 ? 0 : 1;
}
