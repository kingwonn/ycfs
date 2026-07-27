#!/usr/bin/env python3
"""腿:M0-1 同步总线 BOM 与规格自洽(选型可下单、总价在预算、关键规格达标)。

守:
  1. BOM 总价 ≤ 预算(同步总线子系统 ≤ ¥150)。
  2. 每项带型号与渠道(可下单,不是"待定")。
  3. 关键部件满足硬规格:MCU 有硬件时间戳+USB、IMU ≥1kHz、TCXO 温补。
  4. 时基需求自洽:32-bit µs 计数器单调时长 ≥ 需求分钟数(2^32 µs 必须 ≥ min_monotonic)。
  5. 同步误差目标不宽于 cert.py 的阈值(只紧不松:BOM 目标 ≤ 证书阈值)。
输出末行 "结果: N 通过, M 失败"。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BOM = ROOT / "m0" / "bom.json"
PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    check(BOM.exists(), "m0/bom.json 存在")
    if not BOM.exists():
        print(f"结果: {PASSED} 通过, {FAILED} 失败"); sys.exit(1)
    b = json.loads(BOM.read_text(encoding="utf-8"))
    items = b["items"]

    # 1. 总价 ≤ 预算
    total = sum(i["unit_cny"] for i in items)
    budget = b["budget_cny"]
    check(total <= budget, f"BOM 总价 ¥{total} ≤ 预算 ¥{budget}")

    # 2. 每项可下单(型号+渠道非空)
    for i in items:
        check(bool(i.get("model")) and bool(i.get("channel")),
              f"{i['part']} 带型号与渠道(可下单)")

    # 3. 关键部件硬规格
    spec = {i["part"]: i.get("spec", {}) for i in items}
    mcu = spec.get("MCU主控", {})
    check(mcu.get("has_hw_timestamp") is True, "MCU 有硬件时间戳")
    check(mcu.get("has_usb") is True, "MCU 有 USB")
    check(mcu.get("clock_mhz", 0) >= 100, "MCU 主频 ≥100MHz")
    imu = spec.get("IMU", {})
    check(imu.get("sample_hz", 0) >= 1000, "IMU 采样 ≥1kHz")
    tcxo = spec.get("时基晶振", {})
    check(tcxo.get("temp_compensated") is True, "时基晶振温补(长时戳漂移小)")
    led = spec.get("LED时标", {})
    check(led.get("controllable_us") is True, "LED 时标 µs 可控(相机交叉校准)")

    # 4. 时基需求自洽:32-bit µs 计数器单调时长 ≥ 需求
    req = b["requirements"]
    monotonic_min = (2 ** req["counter_bits"]) * req["counter_tick_us"] / 1e6 / 60
    check(monotonic_min >= req["min_monotonic_minutes"],
          f"{req['counter_bits']}-bit µs 计数器单调 {monotonic_min:.0f}min "
          f"≥ 需求 {req['min_monotonic_minutes']}min")

    # 5. 同步目标不宽于证书阈值(只紧不松)
    sys.path.insert(0, str(ROOT / "m0"))
    from cert import THRESHOLDS
    check(req["sync_p99_ms_target"] <= THRESHOLDS["sync_error_p99_ms"],
          f"同步目标 {req['sync_p99_ms_target']}ms ≤ 证书阈值 "
          f"{THRESHOLDS['sync_error_p99_ms']}ms(BOM 目标不宽于证书)")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
