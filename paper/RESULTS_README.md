# Regenerating downstream results

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe paper/generate_results.py
```

The script requires NumPy and Matplotlib. The default input directory is
`ullm_results_2026-10-22/snellius_runs/seed42_lr2e-4`; override it with
`--results PATH` if the exported run directory moves.

It reads the 14 unique run directories, checks that they contain the same ordered
test examples, and independently recalculates accuracy, both exported macro-F1
variants, unparsed counts, all group TPRs and support counts, and both aggregate
TPR-gap measures from predictions. It fails if these do not match the exports.
It does not validate the training datasets or the generation/filtering scores.

Generated outputs:

- `generated/downstream_all.tex`: all 14 models, with each shared baseline once.
- `generated/explanation_pairs.tex`: four matched explanation comparisons.
- `figures/downstream_tpr_gaps.png`: all occupation-level signed TPR gaps and group counts.
- `generated/verified_metrics.json`: full-precision metrics, including individual group TPRs.

The tables are included by `main.tex`. Run the script again after changing its
formatting; manual changes to generated files will be overwritten. The narrative
in `main.tex` is not regenerated and must be reviewed if the input results change.

Reported F1 uses `macro_f1_labels` (28 occupations). Unparsed responses still count
as errors, but are not averaged as an additional target class. Accuracy and F1
are percentages; TPR gaps and paired differences are percentage points. The
exported `macro_f1` is retained in the verified JSON for traceability.

These are single-seed results (42); no significance or across-seed stability is
claimed. The dev/test count discrepancy and learning-rate selection criterion
still need to be documented by the evaluation author.
