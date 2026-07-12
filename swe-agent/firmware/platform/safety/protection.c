#include "protection.h"

void prot_init(prot_ctx_t *ctx)
{
    ctx->state = PROT_RUN;
    ctx->stall_ms = 0u;
    ctx->trip_count = 0u;
}

static void enter_trip(prot_ctx_t *ctx)
{
    if (ctx->state != PROT_TRIP) {
        ctx->trip_count++;
    }
    ctx->state = PROT_TRIP;
    ctx->stall_ms = 0u;
}

prot_state_t prot_step(const prot_thresholds_t *th, const prot_inputs_t *in, prot_ctx_t *ctx)
{
    /* TRIP 闩锁:除显式 prot_reset 外没有任何出边 */
    if (ctx->state == PROT_TRIP) {
        return PROT_TRIP;
    }

    /* 读数无效 = 最危险假设 */
    if (!in->valid) {
        enter_trip(ctx);
        return ctx->state;
    }

    /* 过温 / 过流跳闸 */
    if ((in->temp_c >= th->temp_trip_c) || (in->current_ma >= th->current_trip_ma)) {
        enter_trip(ctx);
        return ctx->state;
    }

    /* 堵转:零转速且有电流,持续超时即跳闸 */
    if ((in->speed_rpm == 0u) && (in->current_ma > 0u)) {
        ctx->stall_ms += in->dt_ms;
        if (ctx->stall_ms >= th->stall_trip_ms) {
            enter_trip(ctx);
            return ctx->state;
        }
    } else {
        ctx->stall_ms = 0u;
    }

    /* 过温降额,带滞回恢复 */
    if (in->temp_c >= th->temp_derate_c) {
        ctx->state = PROT_DERATE;
    } else if (ctx->state == PROT_DERATE && in->temp_c <= th->temp_recover_c) {
        ctx->state = PROT_RUN;
    }

    return ctx->state;
}

bool prot_reset(const prot_thresholds_t *th, const prot_inputs_t *in, prot_ctx_t *ctx)
{
    if (ctx->state != PROT_TRIP) {
        return true;
    }
    if ((!in->valid) || (in->temp_c > th->temp_recover_c)) {
        return false; /* 冷却不足或读数无效,拒绝复位 */
    }
    ctx->state = PROT_RUN;
    ctx->stall_ms = 0u;
    return true;
}
