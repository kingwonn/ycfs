/* test_selftest.c — 60730 自检骨架 host 单测。 */
#include <stdio.h>
#include <string.h>
#include "selftest.h"

static int passed = 0, failed = 0;
#define CHECK(c, n) do { if (c) passed++; else { failed++; printf("FAIL: %s\n", n); } } while (0)

int main(void)
{
    /* T1: CRC-32 已知答案向量(真值锚:标准测试向量,非自产) */
    const char *v = "123456789";
    CHECK(st_crc32((const uint8_t *)v, strlen(v)) == 0xCBF43926u, "T1 CRC32 known-answer");

    /* T2: 空输入 CRC 定义值 */
    CHECK(st_crc32((const uint8_t *)"", 0u) == 0x00000000u, "T2 CRC32 empty");

    /* T3: 表驱动:组件数=12,ID 非空且唯一 */
    size_t n = 0u;
    const st_entry_t *t = st_table(&n);
    CHECK(n == 12u, "T3a 组件数=12(与覆盖表一致)");
    int dup = 0;
    for (size_t i = 0; i < n; i++) {
        for (size_t j = i + 1u; j < n; j++) {
            if (strcmp(t[i].id, t[j].id) == 0) { dup = 1; }
        }
    }
    CHECK(!dup, "T3b 组件 ID 唯一");

    /* T4: 调度如实计数:当前骨架 0 PASS / 0 FAIL / 全 NOT_IMPL(不伪绿) */
    st_summary_t p = st_run_post();
    st_summary_t b = st_run_bist();
    CHECK(p.pass == 0u && p.fail == 0u && p.not_impl > 0u, "T4a POST 如实报 NOT_IMPL");
    CHECK(b.pass == 0u && b.fail == 0u && b.not_impl > 0u, "T4b BIST 如实报 NOT_IMPL");

    printf("RESULT: %d passed, %d failed\n", passed, failed);
    return failed == 0 ? 0 : 1;
}
