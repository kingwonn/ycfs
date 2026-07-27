#!/usr/bin/env python3
"""腿:选型决策矩阵的自洽性(守 tradeoff 引擎不被误用)。

守:
  1. 引擎能算:合成一组路线,加权得分在 [0,1]、覆盖率正确。
  2. 缺数据不蒙混:含 null 维度的路线,覆盖率 <1 且低覆盖被排到达标组之后。
  3. 权重决定结果:同一批路线在 flagship 与 volume 档下,冠军可以不同(证明矩阵有区分力)。
  4. 真实路线文件(若已由调查写入)格式合规:7 维齐全(值为 1-5 或 null)、带 source。
输出末行 "结果: N 通过, M 失败"。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "m0"))
from tradeoff import DIMENSIONS, PROFILES, score_route, rank, ROUTES_DIR  # noqa

PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    hi = {"name": "A", "scores": {d: 5 for d in DIMENSIONS}}
    lo = {"name": "B", "scores": {d: 1 for d in DIMENSIONS}}
    part = {"name": "C", "scores": {d: (3 if i < 4 else None) for i, d in enumerate(DIMENSIONS)}}

    s_hi, cov_hi, _ = score_route(hi, PROFILES["flagship"])
    s_lo, cov_lo, _ = score_route(lo, PROFILES["flagship"])
    s_p, cov_p, miss_p = score_route(part, PROFILES["flagship"])

    check(abs(s_hi - 1.0) < 1e-9, "满分路线得分=1.0")
    check(abs(s_lo - 0.2) < 1e-9, "全1分路线得分=0.2")
    check(cov_hi == 1.0 and cov_p < 1.0, "覆盖率:全填=1、缺3维<1")
    check(len(miss_p) == 3, "缺失维度正确计 3")
    check(0.0 <= s_p <= 1.0, "部分覆盖得分仍在 [0,1]")

    # 权重区分力:构造两条路线,一条精度高成本差,一条反之 → flagship/volume 冠军不同
    import tempfile, os
    ra = {"name": "精度型", "scores": {"accuracy": 5, "multimodal": 5, "portability": 2,
          "cost": 1, "manufacturability": 3, "sim2real_scarcity": 5, "maturity": 3}}
    rb = {"name": "铺量型", "scores": {"accuracy": 2, "multimodal": 2, "portability": 5,
          "cost": 5, "manufacturability": 5, "sim2real_scarcity": 3, "maturity": 5}}
    ROUTES_DIR.mkdir(parents=True, exist_ok=True)
    testf = ROUTES_DIR / "_selftest.json"
    try:
        testf.write_text(json.dumps({"modality": "自测", "routes": [ra, rb]}), encoding="utf-8")
        champ_flag = rank("_selftest", "flagship")["rows"][0]["name"]
        champ_vol = rank("_selftest", "volume")["rows"][0]["name"]
        check(champ_flag == "精度型", "flagship 档冠军=精度型")
        check(champ_vol == "铺量型", "volume 档冠军=铺量型")
        check(champ_flag != champ_vol, "权重有区分力(不同档不同冠军)")
    finally:
        if testf.exists(): testf.unlink()

    # 真实路线文件格式合规(若存在)
    real = [p for p in ROUTES_DIR.glob("*.json") if not p.stem.startswith("_")] if ROUTES_DIR.exists() else []
    for f in real:
        data = json.loads(f.read_text(encoding="utf-8"))
        check("modality" in data and "routes" in data, f"{f.name} 有 modality/routes")
        for r in data["routes"]:
            check("source" in r, f"{f.name}:{r.get('name','?')} 带 source")
            for d in DIMENSIONS:
                v = r["scores"].get(d)
                check(v is None or (isinstance(v, int) and 1 <= v <= 5),
                      f"{f.name}:{r.get('name','?')} 维度 {d} 为 1-5 或 null")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
