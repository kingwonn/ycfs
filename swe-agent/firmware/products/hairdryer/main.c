/*
 * products/hairdryer/main.c — 吹风机产品层入口(门禁种子,非产品固件)。
 * 只 include platform 与 board 接口,不见任何芯片头(gate layer-deps 腿强制)。
 * 任务表节拍参照 docs/hairdryer-tech-plan.md §四:速度环 1kHz / 温度环 50Hz / HMI 10Hz。
 */
#include "board.h"
#include "interlock.h"
#include "protection.h"
#include "sched.h"
#include "thermal_pi.h"

/* PROVENANCE: PLACEHOLDER — 真实阈值必须溯源规格书(L1,卡 D1) */
static const prot_thresholds_t k_th = {
    .temp_derate_c  = 85,
    .temp_trip_c    = 110,
    .temp_recover_c = 70,
    .current_trip_ma = 20000u,
    .stall_trip_ms   = 500u,
};

static volatile int16_t  g_temp_c     = 25;
static volatile uint16_t g_current_ma = 1000u;
static volatile uint32_t g_speed_rpm  = 110000u;

/* PROVENANCE: PLACEHOLDER — 温控/联锁参数须真机标定+规格书溯源(L1) */
static const thermal_cfg_t k_tc = {
    .kp_pm_per_c = 30.0f, .ki_pm_per_c_s = 8.0f, .ff_pm_per_level = 60.0f,
    .out_max_pm = 1000.0f, .hard_limit_c = 115,
};
static const ilk_cfg_t k_ic = {
    .rpm_derate = 60000u, .rpm_cutoff = 30000u, .sustain_ms = 300u,
    .cool_c = 45, .derate_cap_pm = 400u,
};

static prot_ctx_t s_prot;
static thermal_ctx_t s_therm;
static ilk_ctx_t s_ilk;

static void task_speed_1khz(void)
{
    const prot_inputs_t in = {
        .valid = true, .temp_c = g_temp_c, .current_ma = g_current_ma,
        .speed_rpm = g_speed_rpm, .dt_ms = 1u,
    };
    (void)prot_step(&k_th, &in, &s_prot);
}

static void task_thermal_50hz(void)
{
    const uint8_t level = (g_speed_rpm >= 90000u) ? (uint8_t)2u : ((g_speed_rpm >= 60000u) ? (uint8_t)1u : (uint8_t)0u);
    const float cmd = thermal_step(&k_tc, &s_therm, 80, g_temp_c, level, 20u);
    (void)ilk_step(&k_ic, &s_ilk, true, g_speed_rpm, g_temp_c, 20u);
    g_board.heater_permille(ilk_apply(&k_ic, &s_ilk, (uint16_t)cmd));
}

static void task_hmi_10hz(void)
{
    /* 档位/LED 落位处 */
}

static sched_task_t s_tasks[] = {
    { task_speed_1khz,    1u, 0u, "speed"   },
    { task_thermal_50hz, 20u, 0u, "thermal" },
    { task_hmi_10hz,    100u, 0u, "hmi"     },
};

int main(void)
{
    g_board.init();
    prot_init(&s_prot);
    thermal_init(&s_therm);
    ilk_init(&s_ilk);

    sched_t s;
    sched_init(&s, s_tasks, (int)(sizeof s_tasks / sizeof s_tasks[0]), g_board.ticks());

    for (;;) {
        (void)sched_tick(&s, g_board.ticks());
    }
}
