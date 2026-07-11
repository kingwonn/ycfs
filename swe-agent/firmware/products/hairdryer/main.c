/*
 * products/hairdryer/main.c — 吹风机产品层入口(门禁种子,非产品固件)。
 * 只 include platform 与 board 接口,不见任何芯片头(gate layer-deps 腿强制)。
 * 任务表节拍参照 docs/hairdryer-tech-plan.md §四:速度环 1kHz / 温度环 50Hz / HMI 10Hz。
 */
#include "board.h"
#include "protection.h"
#include "sched.h"

/* PROVENANCE: PLACEHOLDER — 真实阈值必须溯源规格书(L1,卡 D1) */
static const prot_thresholds_t k_th = {
    .temp_derate_c  = 85,
    .temp_trip_c    = 110,
    .temp_recover_c = 70,
    .current_trip_ma = 20000u,
    .stall_trip_ms   = 500u,
};

volatile int16_t  g_temp_c     = 25;
volatile uint16_t g_current_ma = 1000u;
volatile uint16_t g_speed_rpm  = 30000u;

static prot_ctx_t s_prot;

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
    /* 温控 PI+前馈落位处(卡 G5);种子阶段空转保持任务表形状 */
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

    sched_t s;
    sched_init(&s, s_tasks, (int)(sizeof s_tasks / sizeof s_tasks[0]), g_board.ticks());

    for (;;) {
        (void)sched_tick(&s, g_board.ticks());
    }
}
