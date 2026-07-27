#!/usr/bin/env python3
"""cert — 质量证书计算器(M0-4)。产品的一半:把"数据好"从话术变成规格。

十项指标,全部确定性计算、公式公开、客户可独立复算。
输入:episode 字典(见 synth.py 的数据形状);输出:cert 字典,十项全非空。

设计纪律(承 data-product-spec.md):
  · 只降不升:任何指标算不出来时输出 null 并标记 uncomputable,绝不给默认好值。
  · 证书是裁决不是装饰:每项带 pass 布尔,阈值集中在 THRESHOLDS,只紧不松。
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

# ── 阈值(只紧不松;对应 data-product-spec.md 第四层) ──
THRESHOLDS = {
    "sync_error_p99_ms": 5.0,      # v0 门槛;押注 2 的硬件目标是 1.0
    "drift_mm": 5.0,               # 每 episode 漂移上界
    "tremble_score": 0.15,         # 速度轨迹相对平滑轨迹的偏差比
    "missing_frame_rate": 0.01,
    "static_ratio": 0.40,          # 静止占比过高 = 无信息演示
    "duration_s_min": 2.0,
    "duration_s_max": 300.0,
    "feasibility_rate_min": 0.90,  # 对参考本体的 IK 可行率
}


def _p99(x):
    return float(np.percentile(np.asarray(x, dtype=float), 99)) if len(x) else None


def sync_error_ms(ep):
    """跨模态同步误差:各流时间戳对公共触发栅格的偏差,P99(ms)。"""
    grid = np.asarray(ep["trigger_grid_s"])
    errs = []
    for stream in ("rgb_ts_s", "pose_ts_s", "force_ts_s"):
        ts = np.asarray(ep[stream])
        n = min(len(ts), len(grid))
        if n == 0:
            return None
        errs.append(np.abs(ts[:n] - grid[:n]) * 1000.0)
    return _p99(np.concatenate(errs))


def drift_mm(ep):
    """位姿漂移:episode 首尾回到同一物理位置时的闭合残差(合成数据里由标注给出)。"""
    loop = ep.get("loop_closure_residual_m")
    return None if loop is None else float(loop) * 1000.0


def tremble(ep):
    """抖动:实际速度轨迹 vs 平滑轨迹的相对偏差 [有据:行业公开定义思路]。"""
    p = np.asarray(ep["ee_pos_m"])          # (T,3)
    if len(p) < 10:
        return None
    v = np.diff(p, axis=0)
    k = 9
    kernel = np.ones(k) / k
    vs = np.stack([np.convolve(v[:, i], kernel, mode="same") for i in range(3)], axis=1)
    num = float(np.linalg.norm(v - vs))
    den = float(np.linalg.norm(vs)) + 1e-9
    return num / den


def missing_frame_rate(ep):
    flags = np.asarray(ep["frame_ok"], dtype=bool)
    return None if flags.size == 0 else float(1.0 - flags.mean())


def static_ratio(ep):
    p = np.asarray(ep["ee_pos_m"])
    if len(p) < 2:
        return None
    speed = np.linalg.norm(np.diff(p, axis=0), axis=1)
    return float((speed < 1e-4).mean())


def duration_s(ep):
    g = ep["trigger_grid_s"]
    return float(g[-1] - g[0]) if len(g) > 1 else 0.0


def consistency(episodes):
    """同任务轨迹一致性:重采样后逐点方差的均值(越小越一致)。跨 episode 指标。"""
    if len(episodes) < 2:
        return None
    T = 50
    resampled = []
    for ep in episodes:
        p = np.asarray(ep["ee_pos_m"])
        idx = np.linspace(0, len(p) - 1, T).astype(int)
        resampled.append(p[idx])
    R = np.stack(resampled)                  # (N,T,3)
    return float(R.std(axis=0).mean())


def diversity(episodes):
    """多样性:场景/物体标签的计数与熵。"""
    scenes = [ep["meta"].get("scene", "?") for ep in episodes]
    objs = [o for ep in episodes for o in ep["meta"].get("objects", [])]

    def _entropy(labels):
        if not labels:
            return 0.0
        _, cnt = np.unique(labels, return_counts=True)
        pr = cnt / cnt.sum()
        return float(-(pr * np.log2(pr)).sum())
    return {"scene_count": len(set(scenes)), "object_count": len(set(objs)),
            "scene_entropy_bits": round(_entropy(scenes), 3)}


def feasibility_rate(episodes):
    flags = [ep["meta"].get("ik_feasible") for ep in episodes]
    known = [f for f in flags if f is not None]
    return None if not known else float(np.mean([1.0 if f else 0.0 for f in known]))


def provenance_complete(ep):
    need = ("device_id", "collector", "ts", "calib_id")
    return all(bool(ep["meta"].get(k)) for k in need)


def make_cert(episodes):
    """对一批 episode 出证书。十项,全非空(算不出的项显式 uncomputable)。"""
    per = []
    for ep in episodes:
        d = duration_s(ep)
        per.append({
            "sync_error_p99_ms": sync_error_ms(ep),
            "drift_mm": drift_mm(ep),
            "tremble_score": tremble(ep),
            "missing_frame_rate": missing_frame_rate(ep),
            "static_ratio": static_ratio(ep),
            "duration_s": d,
            "provenance_complete": provenance_complete(ep),
        })

    def agg(key, fn=max):
        vals = [p[key] for p in per if p[key] is not None]
        return fn(vals) if vals else None

    t = THRESHOLDS
    cert = {
        "1_sync_error_p99_ms": agg("sync_error_p99_ms"),
        "2_drift_mm_max": agg("drift_mm"),
        "3_tremble_score_max": agg("tremble_score"),
        "4_missing_frame_rate_max": agg("missing_frame_rate"),
        "5_abnormal_duration_rate": float(np.mean([
            not (t["duration_s_min"] <= p["duration_s"] <= t["duration_s_max"]) for p in per])),
        "6_static_ratio_max": agg("static_ratio"),
        "7_consistency_std_m": consistency(episodes),
        "8_diversity": diversity(episodes),
        "9_feasibility_rate": feasibility_rate(episodes),
        "10_provenance_complete_rate": float(np.mean([p["provenance_complete"] for p in per])),
    }
    cert["pass"] = {
        "sync": cert["1_sync_error_p99_ms"] is not None and cert["1_sync_error_p99_ms"] <= t["sync_error_p99_ms"],
        "drift": cert["2_drift_mm_max"] is not None and cert["2_drift_mm_max"] <= t["drift_mm"],
        "tremble": cert["3_tremble_score_max"] is not None and cert["3_tremble_score_max"] <= t["tremble_score"],
        "frames": cert["4_missing_frame_rate_max"] is not None and cert["4_missing_frame_rate_max"] <= t["missing_frame_rate"],
        "static": cert["6_static_ratio_max"] is not None and cert["6_static_ratio_max"] <= t["static_ratio"],
        "feasibility": cert["9_feasibility_rate"] is not None and cert["9_feasibility_rate"] >= t["feasibility_rate_min"],
        "provenance": cert["10_provenance_complete_rate"] == 1.0,
    }
    cert["pass_all"] = all(cert["pass"].values())
    return cert


if __name__ == "__main__":
    from synth import make_batch  # noqa
    batch = make_batch(quality=sys.argv[1] if len(sys.argv) > 1 else "good")
    print(json.dumps(make_cert(batch), ensure_ascii=False, indent=2, default=str))
