# Does Access to Generator Explanations Improve Synthetic Data Filtering for Gender Bias Mitigation?

The first paper investigates how bias can be inherited through LLM-generated training data. Building on this setting, we propose to investigate whether access to the generator’s explanations helps an LLM filter select synthetic training examples that lead to lower downstream gender bias while preserving task performance.

## Research question

Does explanation-aware filtering reduce downstream gender bias more effectively than content-only filtering when both methods select the same number of synthetic training examples?

## Dataset and task

We plan to use Bias in Bios, which is also used in the paper Understanding and Mitigating Bias Inheritance in LLM-based Data Augmentation on Downstream Tasks. The downstream task will be occupation classification from biographies, and we will compare how well the model identifies each occupation for men and women.

The experiment uses all 28 occupations. The sampled splits contain 12,000 training, 1,600 development, and 4,000 test examples; see README_Sampling.md for the sampling procedure.

Sampling, synthetic generation, and filtering have been completed, but their full implementation has not yet been merged into main. Downstream training and evaluation remain pending. Generation and filtering implementation details will be documented by the responsible team members.

## Synthetic data generation

The generation design uses only the original training split as a reference. The pipeline uses GPT-4o-mini and Llama-3.1-8B-Instruct for both generation and filtering, following the model choices in the reference paper. Each generator produces a separate pool of approximately 15,000 synthetic biographies (the previously reported exact count of 15,008 remains to be verified). Both filters process each generator pool with and without access to generator explanations.

Each generated record will contain:

- A synthetic biography.
- An occupation label, which can be specified in the generation prompt.
- A gender annotation for distribution analysis.
- A short explanation of the generator’s choices regarding the biography’s content and the person’s attributes.

We use these explanations as extra information, without assuming they reflect how the model actually made its choices.

## Filtering conditions

We will compare three selection strategies applied independently to the same synthetic pool:

1. **Random selection:** randomly select K examples.
2. **Content-only filtering:** an LLM evaluates the biography and occupation label.
3. **Explanation-aware filtering:** the same LLM evaluates the same information together with the generator’s explanation.

Each of the eight filtering branches (two generators x two filters x two explanation-access conditions) retains K = 2,000 examples. Filtering uses the same source pools and reportedly similar prompts; the exact criteria, prompt differences, and controls remain to be documented by the responsible team members. Identical criteria apart from explanation access have not yet been verified.

We will record the occupation and gender distributions of the selected subsets. Whether selection already matches these counts across conditions remains to be confirmed; no additional experimental condition is planned.

## Downstream training

We will fine-tune separate copies of the same initial model under five conditions:

1. Original training data only.
2. Original data plus all synthetic examples.
3. Original data plus the randomly selected subset.
4. Original data plus the content-only filtered subset.
5. Original data plus the explanation-aware filtered subset.

The classification training examples will contain biographies and occupation labels. Generator explanations will be used only for selection and will not be included in downstream training.

There are two random subsets of 2,000 examples and two full-pool baselines, one per generator; these do not depend on the filter model. Together with the eight filtered subsets and one original-only baseline, this yields 13 training-data configurations per downstream model and training seed. The downstream classifier model remains to be specified.

The three K-example conditions will use matched training settings. The full synthetic-data condition will provide an additional reference, with its larger dataset size and training cost reported explicitly.

## Evaluation

All trained models will be evaluated on the same held-out test set. The evaluation protocol is not yet finalized. Candidate measures are:

- Overall occupation-classification performance, such as macro-F1.
- Gender differences in true positive rates within occupations (the likely fairness metric; aggregation remains to be decided).
- Variation across repeated training runs, subject to the final run budget.

Development data will be used to refine prompts and selection settings. The final test set will not be used to choose these settings.

The primary comparison is explanation-aware versus content-only filtering. Random selection tests whether filtering provides a benefit beyond selecting fewer examples, while the original-only and full-pool conditions establish the effects of augmentation.

## Scope

The current study retains the five condition types above. A shuffled-explanation ablation is reserved as a possible future experiment and discussion point for limitations and future work, rather than a scheduled sixth condition.

In that experiment, the filter would receive an explanation from a different synthetic example of the same occupation, with approximately matched length. This could help test whether any benefit depends on the explanation being associated with the specific biography rather than merely providing additional text. Mismatched explanations may also introduce contradictions, so results would require cautious interpretation. Without this control, the current study cannot isolate these effects.

## Potential contribution

The intended contribution is a controlled empirical study of whether generator explanations provide useful information for fairness-oriented synthetic data selection and whether that information translates into improved downstream behavior.

We do not assume that explanation-aware filtering will outperform the alternatives. A negative result could suggest that generator explanations are uninformative or misleading for this purpose under the tested conditions. The novelty of the specific comparison must be established against prior work on bias mitigation through data filtering and explanation-based data selection.