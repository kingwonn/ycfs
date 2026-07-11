/*
 * protection.h — 应用层保护状态机(过温降额/过温跳闸/过流跳闸/堵转跳闸)
 *
 * 纯函数、无副作用、不依赖硬件——可在 host 单测(Ceedling)与目标机上同源编译。
 * 语义:TRIP 为闩锁态,只能经显式 prot_reset() 且满足冷却条件后解除;
 *      任何传感器读数无效(inputs.valid == false)一律视为最危险 → TRIP。
 */
#ifndef PROTECTION_H
#define PROTECTION_H

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    PROT_RUN = 0,   /* 正常运行 */
    PROT_DERATE,    /* 过温降额:限制功率,可自恢复 */
    PROT_TRIP,      /* 跳闸闩锁:输出必须为零,等显式复位 */
} prot_state_t;

typedef struct {
    /* PROVENANCE: PLACEHOLDER — 每个阈值在真实项目中必须溯源到
     * 器件/MCU 规格书某页某表(L1 零编造),溯不到即硬阻断。 */
    int16_t  temp_derate_c;    /* 进入降额的温度阈值 */
    int16_t  temp_trip_c;      /* 过温跳闸阈值(> derate) */
    int16_t  temp_recover_c;   /* 降额恢复阈值(< derate,滞回) */
    uint16_t current_trip_ma;  /* 过流跳闸阈值 */
    uint16_t stall_trip_ms;    /* 堵转(零转速+有电流)持续跳闸时间 */
} prot_thresholds_t;

typedef struct {
    bool     valid;        /* 传感器读数有效性;false → 直接 TRIP */
    int16_t  temp_c;       /* 功率级温度 */
    uint16_t current_ma;   /* 母线电流 */
    uint32_t speed_rpm;    /* 转速(0 = 停转;110k RPM 级,uint16 会回绕 — 域宽 bug 已被 -Werror 抓出) */
    uint16_t dt_ms;        /* 距上次调用的毫秒数 */
} prot_inputs_t;

typedef struct {
    prot_state_t state;
    uint32_t     stall_ms;     /* 堵转累计毫秒 */
    uint32_t     trip_count;   /* 历史跳闸次数(审计) */
} prot_ctx_t;

void         prot_init(prot_ctx_t *ctx);
prot_state_t prot_step(const prot_thresholds_t *th, const prot_inputs_t *in, prot_ctx_t *ctx);
/* 显式复位:仅当当前温度低于恢复阈值才允许离开 TRIP;返回是否复位成功 */
bool         prot_reset(const prot_thresholds_t *th, const prot_inputs_t *in, prot_ctx_t *ctx);

#endif /* PROTECTION_H */
