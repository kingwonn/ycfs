#include "thermal_pi.h"

void thermal_init(thermal_ctx_t *ctx)
{
    ctx->integ_pm = 0.0f;
}

float thermal_step(const thermal_cfg_t *cfg, thermal_ctx_t *ctx,
                   int16_t set_c, int16_t meas_c, uint8_t airflow_level, uint16_t dt_ms)
{
    /* 硬顶:任何情况下测温到线即断热(安全钳,联锁与硬件保险在其后再兜两层) */
    if (meas_c >= cfg->hard_limit_c) {
        return 0.0f;
    }

    const float err = (float)(set_c - meas_c);
    const float dt_s = (float)dt_ms * 0.001f;

    /* 条件积分抗饱和:先算含新积分的输出,若饱和且误差同向,回退本次积分 */
    const float integ_try = ctx->integ_pm + cfg->ki_pm_per_c_s * err * dt_s;
    float out = cfg->kp_pm_per_c * err
              + integ_try
              + cfg->ff_pm_per_level * (float)airflow_level;

    if (out > cfg->out_max_pm) {
        if (err < 0.0f) { ctx->integ_pm = integ_try; }   /* 反向误差仍允许退积分 */
        out = cfg->out_max_pm;
    } else if (out < 0.0f) {
        if (err > 0.0f) { ctx->integ_pm = integ_try; }
        out = 0.0f;
    } else {
        ctx->integ_pm = integ_try;
    }
    return out;
}
