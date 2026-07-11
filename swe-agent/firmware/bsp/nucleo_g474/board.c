/* board.c — NUCLEO-G474 板级实现(种子:无 HAL,SysTick 由裸机计数占位)。 */
#include "board.h"

static volatile uint32_t s_ticks;

static void board_init(void)
{
    /* 种子阶段无时钟树配置;真实板级初始化随 CubeMX/.ioc 引入(卡 G4) */
    s_ticks = 0u;
}

static uint32_t board_ticks(void)
{
    /* 占位:主循环推进;接真 SysTick 后由 1ms 中断递增 */
    return ++s_ticks;
}

const board_ops_t g_board = {
    .init = board_init,
    .ticks = board_ticks,
};

/* OSAL 接缝的裸机实现落在板级 */
uint32_t osal_ticks(void) { return s_ticks; }
