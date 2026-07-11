#include "interlock.h"

void ilk_init(ilk_ctx_t *ctx)
{
    ctx->state = ILK_OK;
    ctx->low_ms = 0u;
    ctx->cutoff_count = 0u;
}

static void enter_cutoff(ilk_ctx_t *ctx)
{
    if (ctx->state != ILK_CUTOFF) {
        ctx->cutoff_count++;
    }
    ctx->state = ILK_CUTOFF;
    ctx->low_ms = 0u;
}

ilk_state_t ilk_step(const ilk_cfg_t *cfg, ilk_ctx_t *ctx,
                     bool valid, uint32_t speed_rpm, int16_t temp_c, uint16_t dt_ms)
{
    /* CUTOFF 闩锁:恢复必须「风量满足 DERATE 线以上」且「已冷却」——双条件缺一不可 */
    if (ctx->state == ILK_CUTOFF) {
        if (valid && speed_rpm >= cfg->rpm_derate && temp_c <= cfg->cool_c) {
            ctx->state = ILK_OK;
            ctx->low_ms = 0u;
        }
        return ctx->state;
    }

    /* 读数无效 = 最危险假设 */
    if (!valid) {
        enter_cutoff(ctx);
        return ctx->state;
    }

    /* 风量丧失:持续超时即切断 */
    if (speed_rpm < cfg->rpm_cutoff) {
        ctx->low_ms += dt_ms;
        if (ctx->low_ms >= cfg->sustain_ms) {
            enter_cutoff(ctx);
            return ctx->state;
        }
    } else {
        ctx->low_ms = 0u;
    }

    ctx->state = (speed_rpm < cfg->rpm_derate) ? ILK_DERATE : ILK_OK;
    return ctx->state;
}

uint16_t ilk_apply(const ilk_cfg_t *cfg, const ilk_ctx_t *ctx, uint16_t cmd_pm)
{
    switch (ctx->state) {
    case ILK_OK:
        return cmd_pm;
    case ILK_DERATE:
        return (cmd_pm > cfg->derate_cap_pm) ? cfg->derate_cap_pm : cmd_pm;
    case ILK_CUTOFF:
    default:
        return 0u;
    }
}
