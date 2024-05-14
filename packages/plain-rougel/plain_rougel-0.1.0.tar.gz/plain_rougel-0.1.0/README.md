# Plain ROUGE-L

Plain ROUGE-L is a Python package designed to compute ROUGE-L scores for evaluating the quality of generated text against reference text. It uses a simple space-based splitting for tokenization. No preprocessing like regex filtering, stemming, etc (useful for some non-English texts). This implementation is approximately 1.5 times faster than the [official ROUGE-L implementation](https://github.com/google-research/google-research/blob/master/rouge/rouge_scorer.py) and supports multiprocessing for batch computations.

## Installation
To install Plain ROUGE-L, simply clone the repository and install dependencies if any.
```bash
git clone https://github.com/oKatanaaa/Plain-ROUGE-L.git
cd Plain-ROUGE-L
pip install .
```

## Usage
Here is a simple example to demonstrate how to use Plain ROUGE-L:

```python
from plain_rougel import RougeLScorer

# Instantiate the scorer
rouge_l_scorer = RougeLScorer()

# Single pair score computation
generated_text = "the cat sat on the mat"
reference_text = "the cat is on the mat"
score = rouge_l_scorer.compute_rouge_l(generated_text, reference_text)
print(score) # Output: {'precision': 0.8, 'recall': 0.8, 'f1': 0.8}

# Batch score computation
generated_texts = ["the cat sat on the mat", "the dog sits on the rug"]
reference_texts = ["the cat is on the mat", "the dog is on the rug"]
batch_scores = rouge_l_scorer.compute_rouge_l_batch(generated_texts, reference_texts)
print(batch_scores) 
# Output: [{'precision': 0.8, 'recall': 0.8, 'f1': 0.8}, {'precision': 0.8, 'recall': 0.8, 'f1': 0.8}]

# Filter generated texts by F-score threshold
filtered_pairs = rouge_l_scorer.filter_by_fscore(generated_texts, reference_texts, fscore_threshold=0.85)
print(filtered_pairs) 
# Output: [('the cat sat on the mat', 'the cat is on the mat', {'precision': 0.8, 'recall': 0.8, 'f1': 0.8}), ('the dog sits on the rug', 'the dog is on the rug', {'precision': 0.8, 'recall': 0.8, 'f1': 0.8})]
```