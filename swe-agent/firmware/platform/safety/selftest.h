/*
 * selftest.h — IEC 60730 Class B 自检调度骨架(B2;表驱动,与 docs/iec60730-coverage.md 一一对应)。
 * 纪律:自检算法不自研(认证走 X-CUBE-STL,见 reuse-landscape);本层只提供
 * 调度框架 + 可在 host 验证的纯函数部件(CRC32);NOT_IMPL 显式上报,绝不伪 PASS。
 */
#ifndef SELFTEST_H
#define SELFTEST_H

#include <stddef.h>
#include <stdint.h>

typedef enum {
    ST_PASS = 0,
    ST_FAIL,
    ST_NOT_IMPL,   /* 显式未实现:调度器如实计数,gate/审计可见——不伪绿 */
} st_result_t;

typedef struct {
    const char  *id;                 /* 与覆盖表组件 ID 一致 */
    st_result_t (*post)(void);       /* 上电自检;NULL=该项无 POST */
    st_result_t (*bist)(void);       /* 周期自检;NULL=该项无 BIST */
} st_entry_t;

typedef struct {
    uint16_t pass;
    uint16_t fail;
    uint16_t not_impl;
} st_summary_t;

/* CRC-32/ISO-HDLC(反射,多项式 0xEDB88320,初值/终值 0xFFFFFFFF)。
 * 已知答案向量:"123456789" → 0xCBF43926(真值锚:CRC 目录标准向量)。 */
uint32_t st_crc32(const uint8_t *data, size_t len);

const st_entry_t *st_table(size_t *n);
st_summary_t      st_run_post(void);
st_summary_t      st_run_bist(void);

#endif /* SELFTEST_H */
