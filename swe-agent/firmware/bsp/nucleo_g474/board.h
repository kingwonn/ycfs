/*
 * board.h — 板级接口(const ops 表,Zephyr device model 式)。
 * products/platform 只见这张函数指针表,不见任何芯片头——「换板不换逻辑」的切面。
 * 种子阶段 ops 为最小集;加热 TRIAC/NTC/HMI 的 ops 随 G5/G4 扩展(只加不减)。
 */
#ifndef BOARD_H
#define BOARD_H

#include <stdint.h>

typedef struct {
    void     (*init)(void);          /* 时钟/引脚/外设初始化 */
    uint32_t (*ticks)(void);         /* 系统节拍(裸机=SysTick 计数) */
    void     (*heater_permille)(uint16_t pm);  /* 加热指令(TRIAC 过零周波调功,种子为存根) */
} board_ops_t;

extern const board_ops_t g_board;    /* 每块板一份 const 实现,编译期绑定置 ROM */

#endif /* BOARD_H */
