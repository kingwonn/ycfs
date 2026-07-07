/*
 * main.c — 门禁种子工程入口(非产品固件)。
 * 用 volatile 假输入驱动保护状态机,防止链接器把逻辑整段优化掉,
 * 保证 .elf 里有真实的 text 段可供 size 断言。
 */
#include "protection.h"

/* PROVENANCE: PLACEHOLDER — 真实阈值必须溯源规格书(见 firmware/README.md) */
static const prot_thresholds_t k_th = {
    .temp_derate_c  = 85,
    .temp_trip_c    = 110,
    .temp_recover_c = 70,
    .current_trip_ma = 20000u,
    .stall_trip_ms   = 500u,
};

volatile int16_t  g_temp_c    = 25;
volatile uint16_t g_current_ma = 1000u;
volatile uint16_t g_speed_rpm  = 30000u;

int main(void)
{
    prot_ctx_t ctx;
    prot_init(&ctx);

    for (;;) {
        const prot_inputs_t in = {
            .valid      = true,
            .temp_c     = g_temp_c,
            .current_ma = g_current_ma,
            .speed_rpm  = g_speed_rpm,
            .dt_ms      = 1u,
        };
        (void)prot_step(&k_th, &in, &ctx);
    }
}
