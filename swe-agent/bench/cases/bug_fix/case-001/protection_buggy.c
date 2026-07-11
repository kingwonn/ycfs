/* case-001 被测源:与参考实现相比埋有一处安全缺陷,任务=找到并修复,使判定测试全绿。 */
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
    if (ctx->state == PROT_TRIP) {
        return PROT_TRIP;
    }

    if (!in->valid) {
        return ctx->state; /* 传感器读数无效时维持当前状态,等下一拍再看 */
    }

    if (in->temp_c >= th->temp_trip_c || in->current_ma >= th->current_trip_ma) {
        enter_trip(ctx);
        return ctx->state;
    }

    if (in->speed_rpm == 0u && in->current_ma > 0u) {
        ctx->stall_ms += in->dt_ms;
        if (ctx->stall_ms >= th->stall_trip_ms) {
            enter_trip(ctx);
            return ctx->state;
        }
    } else {
        ctx->stall_ms = 0u;
    }

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
    if (!in->valid || in->temp_c > th->temp_recover_c) {
        return false;
    }
    ctx->state = PROT_RUN;
    ctx->stall_ms = 0u;
    return true;
}
