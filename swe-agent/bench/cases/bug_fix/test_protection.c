/*
 * test_protection.c — bug_fix 题的判定测试向量(host gcc 可编译)。
 * 出生证:构造于 R8,埋 bug 前对参考实现(firmware/src/protection.c)全绿。
 * 任何一道 bug_fix 题的 buggy 源必须让本测试变红,否则是废题(self-check 会抓)。
 */
#include <stdio.h>
#include "protection.h"

static int failed = 0, passed = 0;
#define CHECK(cond, name) do { \
    if (cond) { passed++; } else { failed++; printf("FAIL: %s\n", name); } \
} while (0)

static const prot_thresholds_t TH = {
    .temp_derate_c = 85, .temp_trip_c = 110, .temp_recover_c = 70,
    .current_trip_ma = 20000u, .stall_trip_ms = 500u,
};

static prot_inputs_t in_ok(void)
{
    prot_inputs_t in = { .valid = true, .temp_c = 25, .current_ma = 1000u,
                         .speed_rpm = 30000u, .dt_ms = 100u };
    return in;
}

int main(void)
{
    prot_ctx_t ctx;
    prot_inputs_t in;

    /* T1: 传感器读数无效 = 最危险假设 → 必须 TRIP */
    prot_init(&ctx);
    in = in_ok(); in.valid = false;
    CHECK(prot_step(&TH, &in, &ctx) == PROT_TRIP, "T1 invalid-sensor→TRIP");

    /* T2: 过温跳闸 + 闩锁(降温后仍 TRIP) */
    prot_init(&ctx);
    in = in_ok(); in.temp_c = 110;
    CHECK(prot_step(&TH, &in, &ctx) == PROT_TRIP, "T2a overtemp→TRIP");
    in = in_ok(); in.temp_c = 25;
    CHECK(prot_step(&TH, &in, &ctx) == PROT_TRIP, "T2b TRIP latches");

    /* T3: 持续堵转 500ms → TRIP */
    prot_init(&ctx);
    in = in_ok(); in.speed_rpm = 0u;
    for (int i = 0; i < 5; i++) { prot_step(&TH, &in, &ctx); }
    CHECK(ctx.state == PROT_TRIP, "T3 sustained-stall→TRIP");

    /* T4: 间歇堵转(每次 <500ms,中间恢复转动)→ 不得误跳闸 */
    prot_init(&ctx);
    for (int round = 0; round < 3; round++) {
        in = in_ok(); in.speed_rpm = 0u;
        for (int i = 0; i < 4; i++) { prot_step(&TH, &in, &ctx); } /* 400ms 堵转 */
        in = in_ok();                                              /* 恢复转动,应清零累计 */
        prot_step(&TH, &in, &ctx);
    }
    CHECK(ctx.state != PROT_TRIP, "T4 intermittent-stall no false trip");

    /* T5: 降额滞回:90→DERATE;75 仍 DERATE;70→RUN */
    prot_init(&ctx);
    in = in_ok(); in.temp_c = 90;
    CHECK(prot_step(&TH, &in, &ctx) == PROT_DERATE, "T5a derate enter");
    in.temp_c = 75;
    CHECK(prot_step(&TH, &in, &ctx) == PROT_DERATE, "T5b hysteresis holds");
    in.temp_c = 70;
    CHECK(prot_step(&TH, &in, &ctx) == PROT_RUN, "T5c recover");

    /* T6: TRIP 后冷却达标才允许复位 */
    prot_init(&ctx);
    in = in_ok(); in.current_ma = 25000u;
    prot_step(&TH, &in, &ctx);
    in = in_ok(); in.temp_c = 90;
    CHECK(!prot_reset(&TH, &in, &ctx), "T6a hot reset refused");
    in.temp_c = 25;
    CHECK(prot_reset(&TH, &in, &ctx) && ctx.state == PROT_RUN, "T6b cool reset ok");

    printf("RESULT: %d passed, %d failed\n", passed, failed);
    return failed == 0 ? 0 : 1;
}
