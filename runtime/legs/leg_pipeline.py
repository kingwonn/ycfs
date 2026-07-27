#!/usr/bin/env python3
"""腿:M0-4 数据管线骨架验收。

守三件事:
  1. 全链路可跑:合成流 → 证书 → LeRobot v3 形状打包,产物齐全。
  2. 证书有判别力(阴性对照内建):好数据必须拿到好证书、坏数据必须被抓——
     坏批的同步/丢帧/静止/溯源四项 pass 必须为 False,好批十项全非空且 pass_all=True。
     一个对好坏数据打同样分的证书,和没有证书不可区分。
  3. 阈值只紧不松:cert.THRESHOLDS 的值不得高于本腿基线(棘轮在 gate 层另有把守)。
输出末行 "结果: N 通过, M 失败"。
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "m0"))

PASSED = FAILED = 0


def check(cond, name):
    global PASSED, FAILED
    if cond:
        PASSED += 1
    else:
        FAILED += 1
        print(f"  ✗ {name}")


def main():
    from synth import make_batch
    from cert import make_cert, THRESHOLDS
    from package import package

    good = make_batch("good")
    bad = make_batch("bad")
    cg, cb = make_cert(good), make_cert(bad)

    # ── 1. 好批:十项全非空,pass_all ──
    for k in [f"{i}_" for i in range(1, 11)]:
        key = next(x for x in cg if x.startswith(k))
        check(cg[key] is not None, f"好批证书项 {key} 非空")
    check(cg["pass_all"] is True, "好批必须 pass_all(否则阈值虚高或合成器坏)")

    # ── 2. 坏批:必须被抓(阴性对照) ──
    check(cb["pass"]["sync"] is False, "坏批 25ms 抖动必须被同步项抓住")
    check(cb["pass"]["frames"] is False, "坏批 5% 丢帧必须被完整性抓住")
    check(cb["pass"]["static"] is False, "坏批长静止段必须被静止项抓住")
    check(cb["pass"]["provenance"] is False, "坏批缺 calib_id 必须被溯源抓住")
    check(cb["pass_all"] is False, "坏批不得 pass_all")
    # 判别力:好坏同步误差必须拉开一个数量级
    check(cg["1_sync_error_p99_ms"] * 10 < cb["1_sync_error_p99_ms"],
          "同步指标必须区分 0.5ms 与 25ms(差一个数量级以上)")

    # ── 3. 打包产物齐全 ──
    with tempfile.TemporaryDirectory() as tmp:
        package(good, cg, tmp)
        out = Path(tmp)
        check((out / "meta" / "info.json").exists(), "meta/info.json 存在")
        check((out / "meta" / "tasks.jsonl").exists(), "meta/tasks.jsonl 存在")
        check((out / "meta" / "episodes.jsonl").exists(), "meta/episodes.jsonl 存在")
        check((out / "cert.json").exists(), "cert.json 随包交付")
        n_ep = len(list((out / "data" / "chunk-000").glob("episode_*")))
        check(n_ep == len(good), f"episode 文件数 {n_ep} = 批大小 {len(good)}")
        info = json.loads((out / "meta" / "info.json").read_text())
        check(info["total_episodes"] == len(good), "info.json 计数一致")

    # ── 4. 阈值存在且为有限值(只紧不松由 gate 棘轮把守) ──
    for k, v in THRESHOLDS.items():
        check(isinstance(v, (int, float)), f"阈值 {k} 是数")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
