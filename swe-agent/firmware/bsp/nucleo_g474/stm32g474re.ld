/* stm32g474re.ld — 链接脚本(门禁种子工程 + J1 分区占位)
 * STM32G474RE: FLASH 512K @ 0x08000000, SRAM1+SRAM2 96K @ 0x20000000 (CCM 未用)
 * 分区(docs/ota-partition-plan.md,待评审签字):
 *   BOOT   0x08000000 32K  — bootloader 预留(种子空置)
 *   APP    0x08008000 472K — 应用镜像(本工程;VTOR 须重定位至此)
 *   PARAMS 0x0807F000 4K   — 标定参数页(J2 落点)
 */
MEMORY
{
  BOOT   (rx)  : ORIGIN = 0x08000000, LENGTH = 32K
  FLASH  (rx)  : ORIGIN = 0x08008000, LENGTH = 472K   /* APP 分区 */
  PARAMS (r)   : ORIGIN = 0x0807F000, LENGTH = 4K
  RAM    (rwx) : ORIGIN = 0x20000000, LENGTH = 96K
}

_estack = ORIGIN(RAM) + LENGTH(RAM);

SECTIONS
{
  .isr_vector : { KEEP(*(.isr_vector)) } > FLASH

  .text : {
    *(.text*)
    *(.rodata*)
    . = ALIGN(4);
  } > FLASH

  _sidata = LOADADDR(.data);
  .data : {
    . = ALIGN(4);
    _sdata = .;
    *(.data*)
    . = ALIGN(4);
    _edata = .;
  } > RAM AT > FLASH

  .bss : {
    . = ALIGN(4);
    _sbss = .;
    *(.bss*)
    *(COMMON)
    . = ALIGN(4);
    _ebss = .;
  } > RAM

  /DISCARD/ : { *(.ARM.exidx*) *(.ARM.attributes) }
}
