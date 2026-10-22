r"""Exploratory occupation/gender analysis; no training or paper edits.

Run: .\.venv\Scripts\python.exe paper/analyze_occupations.py
Outputs JSON with counts, Wilson intervals, confusion counts and paired bootstrap
intervals. Intervals are pointwise, not adjusted for multiple comparisons, and
describe test-sample uncertainty conditional on the fitted models (one seed).
"""
import json
import math
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'ullm_results_2026-10-22/snellius_runs/seed42_lr2e-4'
OUT = ROOT / 'generated/occupation_analysis'


def norm(s):
    return s.strip().replace(' ', '_')


def rate(k, n):
    if not n:
        return {'value': None, 'n': n, 'k': k, 'ci95': None}
    z = 1.959963984540054
    p = k/n
    center = (p+z*z/(2*n))/(1+z*z/n)
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return {'value': p, 'n': n, 'k': k, 'ci95': [center-half, center+half]}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    models = {}
    identity = None
    for folder in sorted(SOURCE.iterdir()):
        if not folder.is_dir():
            continue
        with (folder/'predictions.jsonl').open(encoding='utf-8') as f:
            rows = [json.loads(line) for line in f if line.strip()]
        ids = [(r['hard_text'], norm(r['true']), r['gender']) for r in rows]
        if identity is None:
            identity = ids
        assert ids == identity, 'All comparisons must use identical ordered test records'
        models[folder.name] = np.array([norm(r['pred']) for r in rows])
    truth = np.array([r[1] for r in identity]); gender = np.array([r[2] for r in identity])
    labels = sorted(set(truth))
    detailed = {}
    for name, pred in models.items():
        groups = {}
        for label in labels:
            groups[label] = {}
            for g in ['female', 'male']:
                mask = gender == g; pos = mask & (truth == label); neg = mask & (truth != label)
                tp = int(np.sum(pos & (pred == label))); fp = int(np.sum(neg & (pred == label)))
                errors = Counter(pred[pos & (pred != label)])
                incoming = Counter(truth[neg & (pred == label)])
                groups[label][g] = {
                    'tpr': rate(tp, int(pos.sum())), 'fpr': rate(fp, int(neg.sum())),
                    'precision': rate(tp, int(np.sum(mask & (pred == label)))),
                    'outgoing_errors': dict(errors.most_common()),
                    'incoming_errors': dict(incoming.most_common()),
                    'small_tpr_group': int(pos.sum()) < 30,
                }
            groups[label]['gap'] = groups[label]['female']['tpr']['value']-groups[label]['male']['tpr']['value']
        detailed[name] = groups
    rng = np.random.default_rng(20261022)
    comparisons = {}
    for name, co in models.items():
        if not name.endswith('__3_original_content_only'):
            continue
        prefix = name.split('__')[0]; other = prefix+'__4_original_content_explanation'
        ea = models[other]; results = []
        for label in labels:
            draws = {}; actual = {}; changes = {}
            for g in ['female', 'male']:
                mask = (truth == label) & (gender == g)
                a = (co[mask] == label).astype(int); b = (ea[mask] == label).astype(int)
                n = len(a)
                # Multinomial bootstrap of paired correctness outcomes is exactly
                # equivalent to resampling paired examples within this stratum.
                counts = np.bincount(2*a+b, minlength=4)
                sampled = rng.multinomial(n, counts/n, size=10000)
                da = (sampled[:,2]+sampled[:,3])/n
                db = (sampled[:,1]+sampled[:,3])/n
                draws[g] = (da, db)
                actual[g] = (float(a.mean()), float(b.mean()))
                changes[g] = {'n': n, 'co_tpr': actual[g][0], 'ea_tpr': actual[g][1],
                    'delta': float(b.mean()-a.mean()),
                    'ci95': np.quantile(db-da,[.025,.975]).tolist(),
                    'corrected': int(counts[1]), 'new_errors': int(counts[2])}
            oldgap = actual['female'][0]-actual['male'][0]
            newgap = actual['female'][1]-actual['male'][1]
            change = np.abs(draws['female'][1]-draws['male'][1])-np.abs(draws['female'][0]-draws['male'][0])
            results.append({'occupation': label, 'groups': changes,
                'co_gap': oldgap, 'ea_gap': newgap,
                'delta_abs_gap': abs(newgap)-abs(oldgap),
                'delta_abs_gap_ci95': np.quantile(change,[.025,.975]).tolist(),
                'delta_squared_gap': newgap**2-oldgap**2,
                'small_group': min(changes[g]['n'] for g in changes)<30})
        comparisons[prefix] = results
    metadata = {'test_n':len(identity), 'models':len(models), 'bootstrap_draws':10000,
        'bootstrap_seed':20261022, 'small_group_flag_below':30,
        'interval_note':'95% pointwise intervals, not multiplicity adjusted. Wilson for rates; paired occupation-by-gender stratified percentile bootstrap for changes. Conditional on fitted models; no training-seed uncertainty. Small-group flag is a display aid, not a validity threshold. Unparsed predictions remain errors.'}
    (OUT/'analysis.json').write_text(json.dumps({'metadata':metadata,'models':detailed,'comparisons':comparisons},indent=2),encoding='utf-8')
    lines=['# Exploratory occupation analysis','',metadata['interval_note'],'',
        'All models use the same 3,998 test biographies. Rate intervals retain the actual denominator: true-class support for TPR, other-class support for FPR, and predicted-class support for precision. Raw gender differences in FPR and precision can also reflect different occupation mixtures.','']
    for prefix, rows in comparisons.items():
        lines += ['## '+prefix,'','Changes are explanation-aware minus content-only, in percentage points. Positive changes in absolute gap indicate larger disparity.','',
            '| Occupation | n F/M | TPR F CO→EA | TPR M CO→EA | Δ absolute gap [95% interval] | Small group |',
            '|---|---:|---:|---:|---:|---|']
        for r in sorted(rows,key=lambda r:abs(r['delta_abs_gap']),reverse=True):
            f=r['groups']['female']; m=r['groups']['male']; lo,hi=r['delta_abs_gap_ci95']
            lines.append(f"| {r['occupation']} | {f['n']}/{m['n']} | {100*f['co_tpr']:.1f}→{100*f['ea_tpr']:.1f} | {100*m['co_tpr']:.1f}→{100*m['ea_tpr']:.1f} | {100*r['delta_abs_gap']:+.1f} [{100*lo:+.1f}, {100*hi:+.1f}] | {'yes' if r['small_group'] else 'no'} |")
        lines.append('')
        print(prefix)
        for r in sorted(rows,key=lambda r:abs(r['delta_squared_gap']),reverse=True)[:4]:
            print(r['occupation'],r['groups'],'delta_abs=',round(100*r['delta_abs_gap'],2),'CI=',[round(100*x,2) for x in r['delta_abs_gap_ci95']], 'squared_contribution=',round(r['delta_squared_gap'],5))
    (OUT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    rates = ['# Rates and error destinations by occupation', '', metadata['interval_note'], '',
             'Rates are percentages, followed by numerator/denominator and Wilson 95% interval. Error destinations show counts, not rates. FPR comparisons can reflect different mixtures of other occupations.', '']
    def formatted(value):
        if value['value'] is None:
            return 'undefined (0 denominator)'
        low, high = value['ci95']
        return f"{100*value['value']:.1f} ({value['k']}/{value['n']}; {100*low:.1f}–{100*high:.1f})"
    for name, groups in detailed.items():
        rates += ['## '+name, '', '| Occupation | Gender | TPR | FPR | Precision | Top three error destinations |',
                  '|---|---|---|---|---|---|']
        for label in labels:
            for g in ['female', 'male']:
                row = groups[label][g]
                errors = ', '.join(f"{dest or 'unparsed'}: {count}" for dest, count in list(row['outgoing_errors'].items())[:3]) or 'none'
                rates.append(f"| {label} | {g} | {formatted(row['tpr'])} | {formatted(row['fpr'])} | {formatted(row['precision'])} | {errors} |")
        rates.append('')
    (OUT/'rates.md').write_text('\n'.join(rates)+'\n', encoding='utf-8')
    print('Saved',OUT)


if __name__ == '__main__':
    main()
