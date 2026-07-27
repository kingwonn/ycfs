#!/usr/bin/env python3
"""package — LeRobot v3 形状的打包器(M0-4 骨架)。

按 LeRobotDataset v3 的目录约定组织输出:
    out/
      data/chunk-000/episode_000000.parquet   (无 pyarrow 时降级 .npz,结构等价)
      meta/info.json  meta/tasks.jsonl  meta/episodes.jsonl
      cert.json                                (质量证书,产品的一半)

诚实声明:本骨架保证目录结构与字段命名对齐 v3 约定;
"官方 lerobot loader 零报错读出"这条验收需安装 lerobot(重依赖 torch),
在样机环境完成,本卡状态保持 in-progress 直到那一步跑通——不拿结构等价冒充已验收。
"""
import json
from pathlib import Path

import numpy as np

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    HAS_ARROW = True
except Exception:
    HAS_ARROW = False


def write_episode(out, idx, ep):
    cols = {
        "timestamp": np.asarray(ep["trigger_grid_s"], dtype=np.float64),
        "observation.state.ee_pose_x": ep["ee_pos_m"][:, 0],
        "observation.state.ee_pose_y": ep["ee_pos_m"][:, 1],
        "observation.state.ee_pose_z": ep["ee_pos_m"][:, 2],
        "frame_ok": np.asarray(ep["frame_ok"], dtype=bool),
    }
    d = out / "data" / "chunk-000"
    d.mkdir(parents=True, exist_ok=True)
    if HAS_ARROW:
        pq.write_table(pa.table({k: pa.array(v) for k, v in cols.items()}),
                       d / f"episode_{idx:06d}.parquet")
        return "parquet"
    np.savez(d / f"episode_{idx:06d}.npz", **cols)
    return "npz"


def package(episodes, cert, out_dir, fps=60, task="synthetic manipulation demo"):
    out = Path(out_dir)
    (out / "meta").mkdir(parents=True, exist_ok=True)
    fmt = None
    for i, ep in enumerate(episodes):
        fmt = write_episode(out, i, ep)

    (out / "meta" / "info.json").write_text(json.dumps({
        "codebase_version": "v3.0-shape-compatible",
        "fps": fps, "total_episodes": len(episodes),
        "storage": fmt,
        "features": {
            "observation.state.ee_pose": {"dtype": "float64", "shape": [3]},
            "frame_ok": {"dtype": "bool", "shape": [1]},
        },
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    with open(out / "meta" / "tasks.jsonl", "w", encoding="utf-8") as f:
        f.write(json.dumps({"task_index": 0, "task": task}, ensure_ascii=False) + "\n")
    with open(out / "meta" / "episodes.jsonl", "w", encoding="utf-8") as f:
        for i, ep in enumerate(episodes):
            f.write(json.dumps({"episode_index": i, "length": len(ep["trigger_grid_s"]),
                                "meta": ep["meta"]}, ensure_ascii=False, default=str) + "\n")
    (out / "cert.json").write_text(
        json.dumps(cert, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return fmt
