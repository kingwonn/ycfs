/*
 * thermal_pi.h — 出风温度 PI + 风量前馈(G5,纯函数,host 可测)。
 * 参照 docs/hairdryer-tech-plan.md §四·2:20–100Hz 任务;151°C 角蛋白线之下留硬顶。
 * M4F 带单精度 FPU(-mfloat-abi=hard),控制器用 float 为业界常规。
 */
#ifndef THERMAL_PI_H
#define THERMAL_PI_H

#include <stdint.h>

typedef struct {
    /* PROVENANCE: PLACEHOLDER — 增益与限值须经真机标定/规格书溯源(L1) */
    float    kp_pm_per_c;      /* 比例:permille / °C */
    float    ki_pm_per_c_s;    /* 积分:permille / (°C·s) */
    float    ff_pm_per_level;  /* 风量前馈:permille / 档 */
    float    out_max_pm;       /* 输出上限(=1000) */
    int16_t  hard_limit_c;     /* 硬顶:测温≥此值输出强制 0(安全钳,先于联锁) */
} thermal_cfg_t;

typedef struct {
    float integ_pm;            /* 积分项(已折算到输出域) */
} thermal_ctx_t;

void  thermal_init(thermal_ctx_t *ctx);
/* 返回加热指令 0..out_max_pm(千分比)。条件积分抗饱和:输出饱和方向不再积分。 */
float thermal_step(const thermal_cfg_t *cfg, thermal_ctx_t *ctx,
                   int16_t set_c, int16_t meas_c, uint8_t airflow_level, uint16_t dt_ms);

#endif /* THERMAL_PI_H */
