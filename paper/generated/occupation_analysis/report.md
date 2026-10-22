# Exploratory occupation analysis

95% pointwise intervals, not multiplicity adjusted. Wilson for rates; paired occupation-by-gender stratified percentile bootstrap for changes. Conditional on fitted models; no training-seed uncertainty. Small-group flag is a display aid, not a validity threshold. Unparsed predictions remain errors.

All models use the same 3,998 test biographies. Rate intervals retain the actual denominator: true-class support for TPR, other-class support for FPR, and predicted-class support for precision. Raw gender differences in FPR and precision can also reflect different occupation mixtures.

## GPT-generated-data-GPT-filtering-full

Changes are explanation-aware minus content-only, in percentage points. Positive changes in absolute gap indicate larger disparity.

| Occupation | n F/M | TPR F CO→EA | TPR M CO→EA | Δ absolute gap [95% interval] | Small group |
|---|---:|---:|---:|---:|---|
| chiropractor | 26/74 | 57.7→88.5 | 77.0→85.1 | -16.0 [-35.6, +11.5] | yes |
| architect | 24/78 | 58.3→62.5 | 75.6→64.1 | -15.7 [-25.0, +15.7] | yes |
| yoga_teacher | 84/16 | 92.9→97.6 | 87.5→81.2 | +11.0 [-6.0, +23.5] | yes |
| dj | 14/86 | 78.6→85.7 | 89.5→87.2 | -9.5 [-23.1, +10.6] | yes |
| nurse | 174/17 | 91.4→82.8 | 70.6→70.6 | -8.6 [-12.6, +7.5] | yes |
| pastor | 24/76 | 91.7→95.8 | 90.8→88.2 | +6.8 [-9.6, +12.3] | yes |
| accountant | 37/63 | 70.3→67.6 | 69.8→74.6 | +6.6 [-12.2, +14.9] | no |
| composer | 16/84 | 87.5→87.5 | 97.6→91.7 | -6.0 [-10.7, +8.3] | yes |
| physician | 148/152 | 84.5→79.1 | 64.5→64.5 | -5.4 [-12.7, +1.9] | no |
| model | 83/17 | 88.0→88.0 | 88.2→82.4 | +5.3 [-11.8, +18.4] | yes |
| painter | 46/54 | 89.1→91.3 | 83.3→90.7 | -5.2 [-13.3, +7.4] | no |
| journalist | 99/102 | 84.8→83.8 | 91.2→85.3 | -4.9 [-10.0, +6.2] | no |
| psychologist | 64/39 | 73.4→78.1 | 79.5→79.5 | -4.7 [-12.5, +9.4] | no |
| filmmaker | 33/67 | 87.9→81.8 | 88.1→86.6 | +4.6 [-7.6, +12.2] | no |
| personal_trainer | 46/53 | 89.1→91.3 | 94.3→90.6 | -4.5 [-10.3, +8.4] | no |
| teacher | 83/55 | 60.2→66.3 | 65.5→65.5 | -4.4 [-13.9, +11.5] | no |
| comedian | 21/79 | 76.2→76.2 | 97.5→94.9 | -2.5 [-6.3, +0.0] | yes |
| paralegal | 85/15 | 87.1→84.7 | 66.7→66.7 | -2.4 [-9.4, +4.7] | yes |
| poet | 49/51 | 85.7→91.8 | 76.5→80.4 | +2.2 [-9.6, +12.2] | no |
| dietitian | 93/7 | 91.4→93.5 | 85.7→85.7 | +2.2 [-5.4, +6.5] | yes |
| surgeon | 17/99 | 70.6→64.7 | 87.9→83.8 | +1.8 [-8.0, +15.6] | yes |
| interior_designer | 81/19 | 87.7→87.7 | 89.5→84.2 | +1.6 [-9.8, +14.6] | yes |
| photographer | 71/129 | 93.0→91.5 | 93.0→93.0 | +1.4 [-3.7, +4.9] | no |
| rapper | 10/90 | 90.0→90.0 | 92.2→93.3 | +1.1 [-4.4, +4.4] | yes |
| software_engineer | 16/84 | 81.2→87.5 | 75.0→82.1 | -0.9 [-13.1, +10.4] | yes |
| professor | 271/329 | 89.7→93.4 | 88.4→91.5 | +0.7 [-3.3, +3.4] | no |
| dentist | 51/95 | 90.2→88.2 | 89.5→89.5 | +0.5 [-5.3, +6.2] | no |
| attorney | 77/125 | 85.7→87.0 | 89.6→90.4 | -0.5 [-5.5, +4.7] | no |

## GPT-generated-data-llama-filtering-full

Changes are explanation-aware minus content-only, in percentage points. Positive changes in absolute gap indicate larger disparity.

| Occupation | n F/M | TPR F CO→EA | TPR M CO→EA | Δ absolute gap [95% interval] | Small group |
|---|---:|---:|---:|---:|---|
| dietitian | 93/7 | 92.5→88.2 | 71.4→85.7 | -18.6 [-46.1, +10.4] | yes |
| nurse | 174/17 | 93.7→84.5 | 70.6→76.5 | -15.1 [-28.0, +7.2] | yes |
| attorney | 77/125 | 88.3→77.9 | 90.4→88.0 | +8.0 [-4.1, +15.3] | no |
| yoga_teacher | 84/16 | 96.4→97.6 | 81.2→75.0 | +7.4 [-2.4, +21.7] | yes |
| physician | 148/152 | 81.8→82.4 | 65.1→58.6 | +7.3 [-0.1, +14.6] | no |
| paralegal | 85/15 | 77.6→90.6 | 60.0→80.0 | -7.1 [-29.4, +11.0] | yes |
| rapper | 10/90 | 80.0→90.0 | 91.1→94.4 | -6.7 [-26.7, +6.7] | yes |
| personal_trainer | 46/53 | 93.5→97.8 | 92.5→90.6 | +6.2 [-6.6, +10.6] | no |
| chiropractor | 26/74 | 69.2→80.8 | 82.4→87.8 | -6.1 [-19.2, +6.3] | yes |
| accountant | 37/63 | 67.6→70.3 | 74.6→68.3 | -5.0 [-17.6, +14.5] | no |
| filmmaker | 33/67 | 84.8→81.8 | 91.0→80.6 | -5.0 [-12.6, +13.2] | no |
| teacher | 83/55 | 56.6→61.4 | 65.5→65.5 | -4.8 [-12.7, +7.9] | no |
| comedian | 21/79 | 76.2→81.0 | 96.2→96.2 | -4.8 [-14.3, +0.0] | yes |
| software_engineer | 16/84 | 81.2→87.5 | 82.1→82.1 | +4.5 [-15.2, +13.7] | yes |
| pastor | 24/76 | 87.5→95.8 | 84.2→88.2 | +4.4 [-9.9, +11.2] | yes |
| painter | 46/54 | 89.1→93.5 | 87.0→87.0 | +4.3 [-6.9, +8.7] | no |
| psychologist | 64/39 | 75.0→73.4 | 76.9→79.5 | +4.1 [-9.3, +11.5] | no |
| architect | 24/78 | 62.5→66.7 | 70.5→61.5 | -2.9 [-20.2, +18.6] | yes |
| interior_designer | 81/19 | 88.9→86.4 | 89.5→89.5 | +2.5 [-4.9, +6.2] | yes |
| poet | 49/51 | 85.7→89.8 | 76.5→78.4 | +2.1 [-5.6, +8.2] | no |
| surgeon | 17/99 | 76.5→76.5 | 86.9→84.8 | -2.0 [-6.1, +4.0] | yes |
| model | 83/17 | 89.2→88.0 | 70.6→70.6 | -1.2 [-3.6, +1.2] | yes |
| journalist | 99/102 | 84.8→84.8 | 91.2→92.2 | +1.0 [-5.0, +6.1] | no |
| dentist | 51/95 | 86.3→90.2 | 87.4→88.4 | +0.7 [-7.8, +6.8] | no |
| photographer | 71/129 | 93.0→91.5 | 94.6→93.8 | +0.6 [-4.4, +5.6] | no |
| professor | 271/329 | 91.5→91.5 | 89.7→89.1 | +0.6 [-2.4, +3.2] | no |
| dj | 14/86 | 85.7→92.9 | 88.4→90.7 | -0.5 [-17.3, +9.0] | yes |
| composer | 16/84 | 87.5→87.5 | 95.2→95.2 | +0.0 [-3.6, +3.6] | yes |

## Llama-generated-data-filtering-GPT-full

Changes are explanation-aware minus content-only, in percentage points. Positive changes in absolute gap indicate larger disparity.

| Occupation | n F/M | TPR F CO→EA | TPR M CO→EA | Δ absolute gap [95% interval] | Small group |
|---|---:|---:|---:|---:|---|
| nurse | 174/17 | 91.4→82.8 | 70.6→76.5 | -14.5 [-26.8, +8.9] | yes |
| poet | 49/51 | 91.8→87.8 | 80.4→66.7 | +9.6 [-4.2, +23.2] | no |
| yoga_teacher | 84/16 | 91.7→95.2 | 75.0→87.5 | -8.9 [-26.5, +5.4] | yes |
| rapper | 10/90 | 90.0→80.0 | 92.2→90.0 | +7.8 [-7.8, +26.7] | yes |
| surgeon | 17/99 | 41.2→52.9 | 74.7→78.8 | -7.7 [-30.8, +14.8] | yes |
| chiropractor | 26/74 | 73.1→80.8 | 83.8→83.8 | -7.7 [-18.0, +9.0] | yes |
| filmmaker | 33/67 | 78.8→84.8 | 88.1→88.1 | -6.1 [-15.2, +7.2] | no |
| physician | 148/152 | 87.2→88.5 | 81.6→77.0 | +6.0 [-0.7, +11.9] | no |
| dietitian | 93/7 | 89.2→94.6 | 85.7→85.7 | +5.4 [-8.6, +9.7] | yes |
| accountant | 37/63 | 75.7→73.0 | 74.6→66.7 | +5.2 [-9.5, +12.7] | no |
| teacher | 83/55 | 59.0→56.6 | 63.6→56.4 | -4.3 [-12.7, +11.2] | no |
| personal_trainer | 46/53 | 84.8→87.0 | 90.6→88.7 | -4.1 [-12.4, +8.4] | no |
| dj | 14/86 | 78.6→78.6 | 87.2→90.7 | +3.5 [-15.6, +21.3] | yes |
| psychologist | 64/39 | 75.0→70.3 | 74.4→74.4 | +3.4 [-10.4, +11.9] | no |
| interior_designer | 81/19 | 86.4→85.2 | 78.9→89.5 | -3.2 [-22.3, +13.5] | yes |
| dentist | 51/95 | 86.3→88.2 | 91.6→90.5 | -3.0 [-7.1, +4.3] | no |
| pastor | 24/76 | 83.3→95.8 | 85.5→90.8 | +2.9 [-16.4, +10.1] | yes |
| professor | 271/329 | 91.1→96.7 | 90.0→92.7 | +2.8 [-2.4, +4.9] | no |
| model | 83/17 | 88.0→90.4 | 76.5→76.5 | +2.4 [-3.6, +6.0] | yes |
| software_engineer | 16/84 | 81.2→81.2 | 84.5→82.1 | -2.4 [-7.1, +7.1] | yes |
| composer | 16/84 | 81.2→87.5 | 92.9→97.6 | -1.5 [-22.6, +17.3] | yes |
| attorney | 77/125 | 85.7→84.4 | 88.8→88.8 | +1.3 [-4.7, +6.5] | no |
| architect | 24/78 | 66.7→66.7 | 69.2→62.8 | +1.3 [-14.4, +14.7] | yes |
| comedian | 21/79 | 81.0→81.0 | 94.9→93.7 | -1.3 [-5.1, +2.5] | yes |
| paralegal | 85/15 | 84.7→83.5 | 66.7→66.7 | -1.2 [-5.9, +4.7] | yes |
| photographer | 71/129 | 90.1→88.7 | 93.8→91.5 | -0.9 [-5.4, +5.2] | no |
| painter | 46/54 | 91.3→89.1 | 87.0→85.2 | -0.3 [-6.7, +7.4] | no |
| journalist | 99/102 | 82.8→81.8 | 89.2→88.2 | +0.0 [-5.9, +6.0] | no |

## Llama-generated-data-llama-filtering-full

Changes are explanation-aware minus content-only, in percentage points. Positive changes in absolute gap indicate larger disparity.

| Occupation | n F/M | TPR F CO→EA | TPR M CO→EA | Δ absolute gap [95% interval] | Small group |
|---|---:|---:|---:|---:|---|
| surgeon | 17/99 | 47.1→29.4 | 77.8→76.8 | +16.6 [-1.0, +37.3] | yes |
| model | 83/17 | 86.7→89.2 | 82.4→70.6 | +14.2 [-8.9, +29.1] | yes |
| dietitian | 93/7 | 92.5→90.3 | 85.7→71.4 | +12.1 [-7.5, +39.9] | yes |
| teacher | 83/55 | 51.8→55.4 | 67.3→60.0 | -10.9 [-19.3, +8.5] | no |
| pastor | 24/76 | 91.7→95.8 | 90.8→84.2 | +10.7 [-9.0, +17.5] | yes |
| chiropractor | 26/74 | 80.8→65.4 | 86.5→81.1 | +10.0 [-6.8, +24.2] | yes |
| interior_designer | 81/19 | 86.4→86.4 | 89.5→73.7 | +9.7 [-13.0, +28.8] | yes |
| psychologist | 64/39 | 73.4→60.9 | 74.4→69.2 | +7.4 [-10.9, +16.2] | no |
| nurse | 174/17 | 89.1→82.2 | 70.6→70.6 | -6.9 [-11.5, +6.9] | yes |
| personal_trainer | 46/53 | 84.8→91.3 | 92.5→92.5 | -6.5 [-13.0, +6.5] | no |
| poet | 49/51 | 85.7→75.5 | 74.5→70.6 | -6.3 [-16.3, +10.0] | no |
| physician | 148/152 | 82.4→81.1 | 73.0→66.4 | +5.2 [-2.7, +13.2] | no |
| photographer | 71/129 | 88.7→88.7 | 94.6→90.7 | -3.9 [-9.0, +5.2] | no |
| dj | 14/86 | 78.6→71.4 | 90.7→87.2 | +3.7 [-18.4, +27.4] | yes |
| composer | 16/84 | 81.2→81.2 | 92.9→89.3 | -3.6 [-9.5, +6.0] | yes |
| accountant | 37/63 | 67.6→70.3 | 74.6→66.7 | -3.4 [-17.6, +16.0] | no |
| painter | 46/54 | 80.4→89.1 | 85.2→90.7 | -3.1 [-13.7, +7.8] | no |
| attorney | 77/125 | 83.1→87.0 | 88.0→88.8 | -3.1 [-9.1, +4.8] | no |
| filmmaker | 33/67 | 81.8→75.8 | 92.5→83.6 | -2.9 [-14.9, +12.0] | no |
| software_engineer | 16/84 | 81.2→81.2 | 77.4→79.8 | -2.4 [-16.1, +14.9] | yes |
| comedian | 21/79 | 85.7→81.0 | 97.5→94.9 | +2.2 [-5.1, +13.0] | yes |
| rapper | 10/90 | 90.0→90.0 | 83.3→94.4 | -2.2 [-16.7, +14.4] | yes |
| dentist | 51/95 | 90.2→90.2 | 87.4→89.5 | -2.1 [-8.5, +7.1] | no |
| yoga_teacher | 84/16 | 97.6→98.8 | 75.0→75.0 | +1.2 [-2.4, +4.8] | yes |
| journalist | 99/102 | 82.8→77.8 | 88.2→73.5 | -1.2 [-12.1, +13.6] | no |
| professor | 271/329 | 95.2→97.4 | 93.0→96.4 | -1.1 [-3.8, +1.5] | no |
| paralegal | 85/15 | 84.7→78.8 | 66.7→60.0 | +0.8 [-11.0, +16.5] | yes |
| architect | 24/78 | 62.5→58.3 | 69.2→65.4 | +0.3 [-10.3, +11.9] | yes |

