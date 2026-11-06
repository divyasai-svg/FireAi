from __future__ import annotations

import argparse, json, time
from pathlib import Path
from project_b.core import load_csv, profile
from project_b.inject import PROBLEM_TYPES, inject
from project_b.detectors import rule_detector, statistical_detector, llm_review
from project_b.pipeline import hybrid, detection_metrics

ROOT = Path(__file__).parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(ROOT/'data/sample_311.csv'))
    ap.add_argument('--rows', type=int, default=None)
    args = ap.parse_args()
    rows = load_csv(args.input, args.rows)
    base_profile = profile(rows)
    results = []
    for problem in PROBLEM_TYPES:
        bad, injected = inject(rows, problem, rate=0.25)
        start = time.perf_counter(); rules = rule_detector(bad); rule_ms = (time.perf_counter()-start)*1000
        start = time.perf_counter(); stats = statistical_detector(bad); stat_ms = (time.perf_counter()-start)*1000
        start = time.perf_counter(); out = hybrid(bad); hybrid_ms = (time.perf_counter()-start)*1000
        metric = detection_metrics(out['findings'], injected, problem)
        metric.update({'rule_ms': round(rule_ms, 3), 'statistics_ms': round(stat_ms, 3), 'hybrid_ms': round(hybrid_ms, 3), 'findings': len(out['findings'])})
        results.append(metric)
    report = ROOT/'reports/RESULTS_B.md'
    report.write_text(render_report(args.input, base_profile, results), encoding='utf-8')
    (ROOT/'reports/raw_metrics.json').write_text(json.dumps({'profile': base_profile, 'results': results}, indent=2), encoding='utf-8')
    print(report)

def render_report(source, profile, results):
    lines = ['# Project B results', '', f'Source: `{source}`', '', '## Raw profile', '', f'- Rows: {profile["rows"]}', f'- Columns: {", ".join(profile["columns"])}', f'- Exact duplicate rows in baseline: {profile["exact_duplicate_rows"]}', '', '## Detector comparison', '', '| Problem | Injected | Detected | Detection rate | False alarms | Rules ms | Statistics ms | Hybrid ms |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in results: lines.append(f'| {r["problem"]} | {r["injected"]} | {r["detected"]} | {r["detection_rate"]:.1%} | {r["false_positive"]} | {r["rule_ms"]:.3f} | {r["statistics_ms"]:.3f} | {r["hybrid_ms"]:.3f} |')
    lines += ['', '## Interpretation', '', 'The fixture is intentionally small, so throughput numbers are directional rather than production capacity claims. Run the same command against a representative extract for final capacity figures. Rules run on every row and provide deterministic evidence. Statistics are batch-scoped. The LLM adapter is only reached for candidate rows and is provider-neutral in this offline build; the production Gemini adapter should emit structured JSON with quoted evidence spans and a confidence value.', '', '## Cost model', '', 'Let `N` be rows/day, `p` the fraction flagged by rules/statistics, and `c` the Gemini cost per reviewed row. The hybrid LLM cost is `N × p × c`, versus `N × c` for LLM-on-every-row. The measured routing count is written into `raw_metrics.json` for each run.']
    return '\n'.join(lines) + '\n'

if __name__ == '__main__': main()
