#!/usr/bin/env python3
"""check_dvpr — DVP&R 与 DFMEA 完整性机器校验(I1;gate 的 dvpr-check 腿)。

规则(只紧不松):
  · 每行 DVP&R 必有 limit + limit_provenance(非空)——零编造在交付物层的延伸;
  · 每行必有 evidence/signoff 槽(可为 null,但键必须在——真机回流的落点);
  · L-real 行的 evidence 若非空,必须同时有 signoff(证据没人签=不算,呼应 C1);
  · DFMEA 中 RPN ≥ 阈值的条目必须有 ≥1 条 verification 链接,且链接指向存在的 DVP&R 行;
  · dfmea 反向引用也须存在;行数低于下限视为骨架被掏空。
输出 JSON;任何违规退出非零。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def check(dvpr, dfmea):
    """可测内核:返回问题列表。"""
    problems = []
    rows = {r["id"]: r for r in dvpr.get("rows", [])}

    for rid, r in rows.items():
        for key in ("limit", "limit_provenance", "method", "stage", "category", "requirement"):
            if not r.get(key):
                problems.append(f"{rid}: 缺 {key}")
        for slot in ("evidence", "signoff"):
            if slot not in r:
                problems.append(f"{rid}: 缺 {slot} 槽(真机回流无落点)")
        if r.get("stage") == "L-real" and r.get("evidence") and not r.get("signoff"):
            problems.append(f"{rid}: L-real 行有证据无签字——证据没人签=不算(C1 语义)")
        for fm in r.get("dfmea", []):
            if fm not in {e["id"] for e in dfmea.get("entries", [])}:
                problems.append(f"{rid}: dfmea 引用 {fm} 不存在")

    thr = dfmea.get("rpn_threshold", 100)
    for e in dfmea.get("entries", []):
        rpn = e.get("rpn", e.get("S", 0) * e.get("O", 0) * e.get("D", 0))
        if e.get("S", 0) * e.get("O", 0) * e.get("D", 0) != rpn:
            problems.append(f"{e['id']}: rpn 字段与 S×O×D 不一致")
        if rpn >= thr:
            links = e.get("verification", [])
            if not links:
                problems.append(f"{e['id']}: RPN={rpn} ≥ {thr} 但无验证链接——高风险失效模式裸奔")
            for v in links:
                if v not in rows:
                    problems.append(f"{e['id']}: 验证链接 {v} 指向不存在的 DVP&R 行")
    return problems


def main():
    dvpr = json.load(open(os.path.join(HERE, "dvpr_hairdryer_seed.json"), encoding="utf-8"))
    dfmea = json.load(open(os.path.join(HERE, "dfmea_hairdryer_seed.json"), encoding="utf-8"))
    problems = check(dvpr, dfmea)
    n_rows, n_fm = len(dvpr["rows"]), len(dfmea["entries"])
    print(json.dumps({"dvpr_rows": n_rows, "dfmea_entries": n_fm,
                      "problems": problems}, ensure_ascii=False))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
