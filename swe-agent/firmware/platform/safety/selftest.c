#include "selftest.h"

uint32_t st_crc32(const uint8_t *data, size_t len)
{
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0u; i < len; i++) {
        crc ^= data[i];
        for (int b = 0; b < 8; b++) {
            crc = (crc & 1u) ? ((crc >> 1) ^ 0xEDB88320u) : (crc >> 1);
        }
    }
    return crc ^ 0xFFFFFFFFu;
}

/* ── 各组件自检项:未接 STL 前显式 NOT_IMPL,绝不伪 PASS ── */
static st_result_t st_not_impl(void) { return ST_NOT_IMPL; }

/* FLASH_CRC:纯函数层已实现;APP 区遍历与参考值注入随 G4 接线(种子返回 NOT_IMPL,
 * 防止「算了个空缓冲的 CRC」被当成真自检——宁可少报,不可伪绿)。 */
static st_result_t st_flash_post(void) { return ST_NOT_IMPL; }

static const st_entry_t k_table[] = {
    { "CPU_REG",    st_not_impl,   st_not_impl },
    { "CPU_PC",     NULL,          st_not_impl },
    { "INTERRUPT",  NULL,          st_not_impl },
    { "CLOCK",      NULL,          st_not_impl },
    { "FLASH_CRC",  st_flash_post, st_flash_post },
    { "RAM_MARCH",  st_not_impl,   st_not_impl },
    { "ADDRESSING", st_not_impl,   NULL        },
    { "DATA_PATH",  st_not_impl,   NULL        },
    { "EXT_COMM",   NULL,          st_not_impl },
    { "IO",         NULL,          st_not_impl },
    { "ADC_MUX",    st_not_impl,   st_not_impl },
    { "WDG",        st_not_impl,   st_not_impl },
};

const st_entry_t *st_table(size_t *n)
{
    *n = (sizeof k_table) / (sizeof k_table[0]);
    return k_table;
}

static st_summary_t run(int use_post)
{
    st_summary_t s = { 0u, 0u, 0u };
    for (size_t i = 0u; i < ((sizeof k_table) / (sizeof k_table[0])); i++) {
        st_result_t (*fn)(void) = use_post ? k_table[i].post : k_table[i].bist;
        if (fn == NULL) {
            continue;
        }
        switch (fn()) {
        case ST_PASS:     s.pass++;     break;
        case ST_FAIL:     s.fail++;     break;
        case ST_NOT_IMPL:
        default:          s.not_impl++; break;
        }
    }
    return s;
}

st_summary_t st_run_post(void) { return run(1); }
st_summary_t st_run_bist(void) { return run(0); }
