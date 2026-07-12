# IEC 60730-1 Class B 自检覆盖表(B2 骨架,D-002 授权先行;样例到达后校准)

> 真值锚纪律:每行「措施」锚定**标准条款 + 厂商认证 STL**(X-CUBE-STL,ADOPT 见 reuse-landscape),
> 绝不自研 March/CRC 充数(自研需重走认证)。实现状态只能 NOT_IMPL→STL/IMPL 单向推进(棘轮)。
> 本表与 `firmware/platform/safety/selftest.c` 的组件 ID **一一对应**(gate iec60730-table 腿机器核对)。

| 组件 ID | 组件 | 故障类型 | 可接受措施(H.11.12.7) | POST | BIST | 实现状态 | 真值锚 |
|---|---|---|---|---|---|---|---|
| CPU_REG | CPU 寄存器 | stuck-at | 0x55/0xAA 写读 | ✓ | ✓ | NOT_IMPL(STL 接入位) | IEC 60730-1 H.11.12.7 + X-CUBE-STL |
| CPU_PC | 程序计数器 | stuck-at | 独立时基/逻辑监控 | — | ✓ | NOT_IMPL(STL 接入位) | IEC 60730-1 H.11.12.7 + X-CUBE-STL |
| INTERRUPT | 中断 | 无中断/过频 | 计数×时间窗核对 | — | ✓ | NOT_IMPL | IEC 60730-1 H.11.12.7 |
| CLOCK | 时钟 | 错频 | 独立时基频率监测 | — | ✓ | NOT_IMPL | IEC 60730-1 H.11.12.7 |
| FLASH_CRC | 不变存储器 | 单比特错 | CRC 校验 | ✓ | ✓ | IMPL(纯函数 CRC32,APP 区遍历随 G4 接线) | IEC 60730-1 H.11.12.7;CRC-32/ISO-HDLC 已知答案向量 |
| RAM_MARCH | 可变存储器 | DC 故障 | March 测试 | ✓ | ✓ | NOT_IMPL(STL 接入位,不自研) | IEC 60730-1 H.11.12.7 + X-CUBE-STL |
| ADDRESSING | 寻址 | stuck-at | 地址线测试 | ✓ | — | NOT_IMPL(STL 接入位) | IEC 60730-1 H.11.12.7 + X-CUBE-STL |
| DATA_PATH | 内部数据通路 | stuck-at | 测试图样 | ✓ | — | NOT_IMPL(STL 接入位) | IEC 60730-1 H.11.12.7 + X-CUBE-STL |
| EXT_COMM | 外部通信 | 哈明距离 3 | CRC/冗余 | — | ✓ | NOT_IMPL(产品级,随通信协议定) | IEC 60730-1 H.11.12.7 |
| IO | I/O 外设 | 异常 | 合理性检查 | — | ✓ | NOT_IMPL(联锁已部分承担,正式判定待表校准) | IEC 60730-1 H.11.12.7 |
| ADC_MUX | 模拟/ADC | 漂移/卡值 | 已知基准回读 | ✓ | ✓ | NOT_IMPL(随 G4 ADC 配置) | IEC 60730-1 H.11.12.7 |
| WDG | 独立看门狗 | 失效 | 窗口喂狗+复位验证 | ✓ | 运行时 | NOT_IMPL(随 G4 IWDG 配置) | IEC 60730-1 H.11.12.7 |

## 防自证纪律(常备)

- 期望值(如 FLASH CRC 参考值)**由构建管线独立计算**注入,绝不取运行时自身输出回填;
- 字节同源探针随 L0 真值管道接入(bench 已有同款机制);
- 本表形态为骨架:**Q2 老项目样例到达后触发前提重审**(D-002)。

## 棘轮

| 轮 | IMPL 数 | 备注 |
|---|---|---|
| R18 基线 | 1(FLASH_CRC 纯函数层) | 只增不减;STL 接入随 G4 |
