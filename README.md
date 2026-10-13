# Does Access to Generator Explanations Improve Synthetic Data Filtering for Gender Bias Mitigation?

The first paper investigates how bias can be inherited through LLM-generated training data. Building on this setting, we propose to investigate whether access to the generator’s explanations helps an LLM filter select synthetic training examples that lead to lower downstream gender bias while preserving task performance.

## Research question

Does explanation-aware filtering reduce downstream gender bias more effectively than content-only filtering when both methods select the same number of synthetic training examples?

## Dataset and task

We plan to use Bias in Bios, which is also used in the paper Understanding and Mitigating Bias Inheritance in LLM-based Data Augmentation on Downstream Tasks. The downstream task will be occupation classification from biographies, and we will compare how well the model identifies each occupation for men and women.

We may restrict the experiment to a subset of occupations.

## Synthetic data generation

Using only the original data from the training split as a reference, an LLM will generate a shared pool of synthetic biographies, for example 10,000 examples, potentially more depending on the size of the training dataset.

Each generated record will contain:

- A synthetic biography.
- An occupation label, which can be specified in the generation prompt.
- A gender annotation for distribution analysis.
- A short explanation of the generator’s choices regarding the biography’s content and the person’s attributes.

We will use these explanations as extra information, without assuming they reflect how the model actually made its choices. We will first run a small pilot to check whether they provide useful details about each generated example.

## Filtering conditions

We will compare three selection strategies applied independently to the same synthetic pool:

1. **Random selection:** randomly select K examples.
2. **Content-only filtering:** an LLM evaluates the biography and occupation label.
3. **Explanation-aware filtering:** the same LLM evaluates the same information together with the generator’s explanation.

Both LLM filters will use the same evaluation criteria, covering stereotypical content, relevance, and consistency with the occupation label. Each strategy will retain the same number of examples, for example 2,000 out of 10,000.

We will record the occupation and gender distributions of the selected subsets. A comparison with matched occupation and gender counts will help distinguish the contribution of the explanations from changes in group representation alone.

## Downstream training

We will fine-tune separate copies of the same initial model under five conditions:

1. Original training data only.
2. Original data plus all synthetic examples.
3. Original data plus the randomly selected subset.
4. Original data plus the content-only filtered subset.
5. Original data plus the explanation-aware filtered subset.

The classification training examples will contain biographies and occupation labels. Generator explanations will be used only for selection and will not be included in downstream training.

The three K-example conditions will use matched training settings. The full synthetic-data condition will provide an additional reference, with its larger dataset size and training cost reported explicitly.

## Evaluation

All trained models will be evaluated on the same held-out test set. We will measure:

- Overall occupation-classification performance, such as macro-F1.
- Gender differences in true positive rates within occupations.
- Variation across repeated training runs.

Development data will be used to refine prompts and selection settings. The final test set will not be used to choose these settings.

The primary comparison is explanation-aware versus content-only filtering. Random selection tests whether filtering provides a benefit beyond selecting fewer examples, while the original-only and full-pool conditions establish the effects of augmentation.

## Shuffled explanations

If needed, we will add a condition in which the filter receives an explanation from a different synthetic example of the same occupation, with approximately matched length.

This tests whether any benefit depends on the explanation being associated with the specific example, rather than merely providing additional text. Results will be interpreted cautiously because mismatched explanations may also introduce contradictions.

## Potential contribution

The intended contribution is a controlled empirical study of whether generator explanations provide useful information for fairness-oriented synthetic data selection and whether that information translates into improved downstream behavior.

We do not assume that explanation-aware filtering will outperform the alternatives. A negative result could suggest that generator explanations are uninformative or misleading for this purpose under the tested conditions. The novelty of the specific comparison must be established against prior work on bias mitigation through data filtering and explanation-based data selection.

## Repository guide

- [README_Sampling.md](README_Sampling.md): sampling the Bias in Bios train/dev/test splits.
- [README_Generation.md](README_Generation.md): the synthetic data generation pipeline (setup, API keys, commands, outputs, pilot results).
- [llm_api/README.md](llm_api/README.md): shared code for calling Llama and GPT-4o-mini (used by generation, reusable for filtering), API key sharing, usage and cost.
