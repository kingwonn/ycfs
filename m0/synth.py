#!/usr/bin/env python3
"""synth — 合成数据流(M0-4 骨架验证用)。

在没有硬件之前,用可控的合成 episode 打通"采集→证书→打包"全链路,
并给证书计算器提供已知好/坏对照(坏数据必须拿到坏证书——阴性对照原则)。

quality:
  good — 模拟达标设备:同步误差 ~0.5ms、无丢帧、平滑轨迹、完整溯源
  bad  — 模拟消费级方案:同步抖动 ~25ms、丢帧、抖动轨迹、静止段、溯源缺失
"""
import numpy as np

RNG = np.random.default_rng(7)  # 固定种子:证书数字可复现


def make_episode(quality="good", T=240, hz=60.0, scene="kitchen", objects=("cup", "plate")):
    grid = np.arange(T) / hz
    jitter_ms = 25.0 if quality == "bad" else 0.5

    def jittered():
        return grid + RNG.normal(0, jitter_ms / 1000.0, size=T)

    # 平滑基准轨迹(最小加加速度样式的圆弧)
    t = np.linspace(0, 1, T)
    base = np.stack([0.3 * np.sin(2 * np.pi * t), 0.3 * np.cos(2 * np.pi * t), 0.1 * t], axis=1)
    if quality == "bad":
        base = base + RNG.normal(0, 0.004, size=base.shape)     # 手抖
        base[int(T * 0.50):int(T * 0.95)] = base[int(T * 0.50)]  # 长静止段(45%,须超 40% 阈值被抓)

    frame_ok = np.ones(T, dtype=bool)
    if quality == "bad":
        frame_ok[RNG.choice(T, size=int(T * 0.05), replace=False)] = False

    meta = {"scene": scene, "objects": list(objects), "ik_feasible": True,
            "device_id": "M0-PROTO-001", "collector": "synth", "ts": "2026-07-26",
            "calib_id": "CAL-0001"}
    if quality == "bad":
        meta.pop("calib_id")            # 溯源缺失
        meta["ik_feasible"] = bool(RNG.random() > 0.4)

    return {
        "trigger_grid_s": grid,
        "rgb_ts_s": jittered(), "pose_ts_s": jittered(), "force_ts_s": jittered(),
        "ee_pos_m": base,
        "frame_ok": frame_ok,
        "loop_closure_residual_m": 0.002 if quality == "good" else 0.012,
        "meta": meta,
    }


def make_batch(quality="good", n=6):
    scenes = ["kitchen", "desk", "shelf"] if quality == "good" else ["kitchen"]
    return [make_episode(quality, scene=scenes[i % len(scenes)],
                         objects=("cup", "plate", "bottle")[: 2 + i % 2]) for i in range(n)]
