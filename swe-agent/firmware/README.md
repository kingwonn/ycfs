# firmware — 交叉编译门禁种子工程(STM32G474,Cortex-M4F)

> **这不是产品固件。** 这是 F1 卡「可编译通过」门禁的最小可验证载体:
> 一个能被 arm-none-eabi-gcc 无头构建出 .elf/.map/size 报告的 STM32G4 裸机工程,
> 外加一个**真实形态**的应用层保护状态机(`src/protection.c`)——按 D-001 立法,
> 这类应用层保护逻辑正是 agent 的 coding 表面积(电机环由 MCSDK workbench 生成,不在此)。

## 构建(一条命令)

```bash
./build.sh          # cmake 配置 + 构建 → build/firmware.elf / firmware.map / size 报告
```

## 门禁接线

`../gate.py` 的 `cross-compile` 腿会:
1. 校验 `arm-none-eabi-gcc -dumpversion` 与 `toolchain.lock` 一致(不一致即红——可复现性);
2. 跑 `./build.sh`;
3. 断言 `firmware.elf`/`firmware.map` 存在、`size` 输出可解析、text 段非零且 flash 占用在预算内。

## 零编造纪律

`src/protection.c` 里的所有阈值都标注了 `PROVENANCE: PLACEHOLDER`——
在 L1 溯源管道(卡 D1)落地前,**任何阈值都不得声称来自规格书**。
真实项目中,每个阈值必须溯源到器件/MCU 规格书某页某表,溯不到即硬阻断。
