/*
 * interlock.h — 电机-加热联锁(G5,软件安全核心;60335-2-23 语义,专利谱系 US4003388A)。
 * 规则:风量不足 → 加热先降档(DERATE)后切断(CUTOFF);CUTOFF 闩锁,
 * 恢复必须同时满足「风量已恢复」且「已冷却」;传感器读数无效 = 最危险假设 → 立即 CUTOFF。
 * 纯整数、无副作用,host 单测 + bench 埋 bug 题覆盖。
 */
#ifndef INTERLOCK_H
#define INTERLOCK_H

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    ILK_OK = 0,      /* 风量正常,加热不受限 */
    ILK_DERATE,      /* 风量偏低,加热限幅 */
    ILK_CUTOFF,      /* 风量丧失/读数无效,加热为零,闩锁 */
} ilk_state_t;

typedef struct {
    /* PROVENANCE: PLACEHOLDER — 阈值须溯源风道热设计/规格书(L1) */
    uint16_t rpm_derate;      /* 低于此转速进入 DERATE */
    uint16_t rpm_cutoff;      /* 低于此转速开始累计切断计时 */
    uint16_t sustain_ms;      /* 低风量持续多久执行 CUTOFF */
    int16_t  cool_c;          /* 恢复所需的冷却温度上限 */
    uint16_t derate_cap_pm;   /* DERATE 态加热上限(千分比) */
} ilk_cfg_t;

typedef struct {
    ilk_state_t state;
    uint32_t    low_ms;       /* 低风量累计 */
    uint32_t    cutoff_count; /* 历史切断次数(审计) */
} ilk_ctx_t;

void        ilk_init(ilk_ctx_t *ctx);
ilk_state_t ilk_step(const ilk_cfg_t *cfg, ilk_ctx_t *ctx,
                     bool valid, uint32_t speed_rpm, int16_t temp_c, uint16_t dt_ms);
/* 把温控指令按联锁状态钳制成实际允许的加热指令 */
uint16_t    ilk_apply(const ilk_cfg_t *cfg, const ilk_ctx_t *ctx, uint16_t cmd_pm);

#endif /* INTERLOCK_H */
