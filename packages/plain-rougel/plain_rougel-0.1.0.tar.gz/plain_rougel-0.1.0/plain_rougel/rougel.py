from multiprocessing import Pool, cpu_count


def _lcs_length(ref, can):
    """Compute the length of the Longest Common Subsequence (LCS)."""
    if len(ref) < len(can):
        ref, can = can, ref

    previous = [0] * (len(can) + 1)
    current = [0] * (len(can) + 1)

    for i in range(1, len(ref) + 1):
        for j in range(1, len(can) + 1):
            if ref[i - 1] == can[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous, current = current, previous

    return previous[-1]


class RougeLScorer:
    def __init__(self, n_processes=None):
        self.n_processes = n_processes
        if self.n_processes is None:
            self.n_processes = cpu_count()

    def preprocess_text(self, text):
        return text.split()

    def compute_rouge_l(self, generated, reference):
        generated = self.preprocess_text(generated)
        reference = self.preprocess_text(reference)
        lcs_length = _lcs_length(reference, generated)
        precision = lcs_length / len(generated) if generated else 0.0
        recall = lcs_length / len(reference) if reference else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    def compute_rouge_l_batch(self, generated_list, reference_list):
        assert len(generated_list) == len(reference_list), "The lists must be of the same length"
        
        with Pool(self.n_processes) as pool:
            results = pool.starmap(self.compute_rouge_l, zip(generated_list, reference_list))
        
        return results

    def filter_by_fscore(self, generated_list, reference_list, fscore_threshold):
        assert len(generated_list) == len(reference_list), "The lists must be of the same length"
        
        with Pool(cpu_count()) as pool:
            results = pool.starmap(self.compute_rouge_l, zip(generated_list, reference_list))
        
        filtered_pairs = [(gen, ref, score) for gen, ref, score in zip(generated_list, reference_list, results) if score['f1'] < fscore_threshold]
        
        return filtered_pairs
