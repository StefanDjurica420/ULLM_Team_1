"""Validate exported predictions and regenerate paper tables and the TPR-gap figure.

Run from the repository root: python paper/generate_results.py
Requires matplotlib and numpy. Input files are read-only.
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PAPER = Path(__file__).resolve().parent
PREFIXES = [
    'GPT-generated-data-GPT-filtering-full',
    'GPT-generated-data-llama-filtering-full',
    'Llama-generated-data-filtering-GPT-full',
    'Llama-generated-data-llama-filtering-full',
]


def norm(value):
    return value.strip().replace(' ', '_')


def close(actual, expected, name):
    if not math.isclose(actual, expected, abs_tol=1e-10):
        raise ValueError(f'{name}: recomputed {actual}, exported {expected}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, default=PAPER.parent / 'ullm_results_2026-10-22/snellius_runs/seed42_lr2e-4')
    args = parser.parse_args()
    records = {}
    reference = None
    for directory in sorted(args.results.iterdir()):
        if not directory.is_dir():
            continue
        m = json.loads((directory / 'metrics.json').read_text(encoding='utf-8'))
        config = json.loads((directory / 'config.json').read_text(encoding='utf-8'))
        with (directory / 'predictions.jsonl').open(encoding='utf-8') as handle:
            rows = [json.loads(line) for line in handle if line.strip()]
        identity = [(r['hard_text'], norm(r['true']), r['gender']) for r in rows]
        if reference is None:
            reference = identity
        if identity != reference:
            raise ValueError(f'Different test examples/order: {directory.name}')
        if len(rows) != m['n'] or config['seed'] != 42:
            raise ValueError(f'Unexpected test count or seed: {directory.name}')
        labels = [norm(x) for x in config['labels']]
        if len(set(labels)) != 28:
            raise ValueError('Expected 28 distinct labels')
        truth = Counter(norm(r['true']) for r in rows)
        predicted = Counter(norm(r['pred']) for r in rows)
        correct = Counter(norm(r['true']) for r in rows if norm(r['pred']) == norm(r['true']))
        f1 = lambda label: 2 * correct[label] / (truth[label] + predicted[label]) if truth[label] + predicted[label] else 0
        close(sum(correct.values()) / len(rows), m['accuracy'], 'accuracy')
        close(sum(f1(x) for x in labels) / 28, m['macro_f1_labels'], 'F1 over 28 labels')
        union = set(truth) | set(predicted)
        close(sum(f1(x) for x in union) / len(union), m['macro_f1'], 'exported F1')
        if predicted[''] != m['unparsed']:
            raise ValueError('Unparsed count mismatch')
        gaps = []
        for label in labels:
            rates = {}
            for gender in ['female', 'male']:
                group = [r for r in rows if norm(r['true']) == label and r['gender'] == gender]
                exported = m['tpr_per_group'][f'{label}_{gender}']
                if not group or len(group) != exported['n']:
                    raise ValueError('Missing group or support mismatch')
                rates[gender] = sum(norm(r['pred']) == label for r in group) / len(group)
                close(rates[gender], exported['tpr'], f'{label} {gender} TPR')
            gap = rates['female'] - rates['male']
            close(gap, m['tpr_gap_female_minus_male'][label], 'TPR gap')
            gaps.append(gap)
        close(math.sqrt(sum(x*x for x in gaps) / 28), m['tpr_gap_rms'], 'RMS gap')
        close(sum(abs(x) for x in gaps) / 28, m['tpr_gap_mean_abs'], 'Mean absolute gap')
        records[directory.name] = m

    # Explicit ordering: shared baselines occur only once, never as repeated runs.
    specs = [('0_base_model', '--', '--', 'Base model'), ('1_original', '--', '--', 'Original only')]
    for generator, prefix in [('GPT', PREFIXES[0]), ('Llama', PREFIXES[2])]:
        specs.extend([(prefix+'__2_original_all', generator, '--', 'Full pool'),
                      (prefix+'__5_original_random', generator, '--', 'Random')])
    for prefix, generator, scorer in zip(PREFIXES, ['GPT','GPT','Llama','Llama'], ['GPT','Llama','GPT','Llama']):
        specs.extend([(prefix+'__3_original_content_only', generator, scorer, 'Content only'),
                      (prefix+'__4_original_content_explanation', generator, scorer, 'Explanation aware')])
    if set(records) != {s[0] for s in specs}:
        raise ValueError('Expected exactly the 14 exported configurations')
    out = PAPER / 'generated'
    figures = PAPER / 'figures'
    out.mkdir(exist_ok=True)
    figures.mkdir(exist_ok=True)
    lines = [r'\begin{table*}[t]', r'\centering', r'\small',
        r'\caption{Classification performance and gender TPR gaps. Accuracy and macro F1 are percentages; gaps are in percentage points.}',
        r'\label{tab:downstream-all}', r'\begin{tabular}{lllrrrrr}', r'\toprule',
        r'Generator & Filter & Training condition & Accuracy & Macro F1 & RMS gap & MA gap & Unparsed \\', r'\midrule']
    for index, (key, generator, scorer, condition) in enumerate(specs):
        if index in [2, 6]:
            lines.append(r'\midrule')
        m = records[key]
        values = ' & '.join(f'{100*m[x]:.2f}' for x in ['accuracy','macro_f1_labels','tpr_gap_rms','tpr_gap_mean_abs'])
        lines.append(f'{generator} & {scorer} & {condition} & {values} & {m["unparsed"]} '+r'\\')
    lines += [r'\bottomrule', r'\end{tabular}', r'\end{table*}']
    (out/'downstream_all.tex').write_text('\n'.join(lines)+'\n', encoding='utf-8')

    lines = [r'\begin{table}[H]', r'\centering', r'\small', r'\setlength{\tabcolsep}{3pt}',
        r'\caption{Effect of generator explanations on macro F1 and RMS TPR gaps. CO: content only; EA: explanation aware. Differences ($\Delta$) are EA minus CO, in percentage points.}',
        r'\label{tab:explanation-pairs}', r'\begin{tabular}{@{}lrrrrrr@{}}', r'\toprule',
        r' & \multicolumn{3}{c}{Macro F1} & \multicolumn{3}{c}{RMS TPR gap} \\', r'\cmidrule(lr){2-4}\cmidrule(l){5-7}', r'Gen./filter & CO & EA & $\Delta$ & CO & EA & $\Delta$ \\', r'\midrule']
    for prefix, generator, scorer in zip(PREFIXES, ['GPT','GPT','Llama','Llama'], ['GPT','Llama','GPT','Llama']):
        a = records[prefix+'__3_original_content_only']; b = records[prefix+'__4_original_content_explanation']
        values = []
        for metric in ['macro_f1_labels', 'tpr_gap_rms']:
            values += [f'{100*a[metric]:.2f}', f'{100*b[metric]:.2f}', f'{100*(b[metric]-a[metric]):+.2f}']
        lines.append(f'{generator}/{scorer} & '+' & '.join(values)+r' \\')
    lines += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
    (out/'explanation_pairs.tex').write_text('\n'.join(lines)+'\n', encoding='utf-8')

    occupations = sorted(records['1_original']['tpr_gap_female_minus_male'])
    data = np.array([[100*records[key]['tpr_gap_female_minus_male'][p] for key, *_ in specs] for p in occupations])
    limit = math.ceil(float(np.abs(data).max()) / 5) * 5
    column_labels = ['Base', 'Original', 'GPT full', 'GPT random', 'Llama full', 'Llama random',
                     'G/G CO','G/G EA','G/L CO','G/L EA','L/G CO','L/G EA','L/L CO','L/L EA']
    supports = records['1_original']['tpr_per_group']
    row_labels = [f'{p.replace("_", " ")} ({supports[p+"_female"]["n"]}/{supports[p+"_male"]["n"]})' for p in occupations]
    fig, ax = plt.subplots(figsize=(11, 4.7), layout='constrained')
    im = ax.imshow(data.T, cmap='RdBu_r', vmin=-limit, vmax=limit, aspect='auto')
    ax.set_xticks(range(28), row_labels, rotation=65, ha='right', fontsize=8)
    ax.set_yticks(range(14), column_labels, fontsize=9)
    ax.set_xlabel('Occupation (female / male test counts)', fontsize=9)
    for boundary in [1.5, 5.5, 7.5, 9.5, 11.5]:
        ax.axhline(boundary, color='white', linewidth=1.3)
    fig.colorbar(im, ax=ax, shrink=.75, label='TPR gap (pp)')
    fig.savefig(figures/'downstream_tpr_gaps.png', dpi=220)
    plt.close(fig)
    # Retain full precision, including all group-level TPRs and denominators.
    (out/'verified_metrics.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')
    print(f'Validated {len(records)} models on {len(reference)} identical test records; all metrics match predictions.')
    print('Generated two LaTeX tables, the TPR-gap figure, and verified_metrics.json.')


if __name__ == '__main__':
    main()
