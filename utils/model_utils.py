import re
from sentence_transformers import SentenceTransformer, util
from langdetect import detect, DetectorFactory

class EvaluatorModel:
    def __init__(self, model):
        self.model = SentenceTransformer(model)
        DetectorFactory.seed = 0
 
    def normalize(self, text):
        """Normalizes the text by lowercasing and stripping the punctuation at ends."""
        regex = r'[^\w\s]'
        return re.sub(regex, '', text.lower().strip())

    def is_wrong_answer(self, semantic_score):
        return semantic_score < 30

    def is_one_line(self, text):
        return len(self.normalize(text).split()) <= 7

    def is_incomplete(self, text):
        regex = r'[.!?]$'
        return not re.search(regex, text.strip()) or len(self.normalize(text).split()) < 5

    def is_gibberish(self, text):
        try:
            lang = detect(text)
            return lang not in ["en"]
        except:
            return True

    def compute_semantic_similarity(self, base, compare):
        """Compute the semantic similarity between the sample answer and the user answer"""
        base = self.normalize(base)
        compare = self.normalize(compare)
        if self.is_gibberish(base) or self.is_gibberish(compare):
            return 0.0
        base_emb = self.model.encode(base, convert_to_tensor=True)
        compare_emb = self.model.encode(compare, convert_to_tensor=True)
        score = util.pytorch_cos_sim(base_emb, compare_emb).item()
        return round(score * 100, 2)

    def compute_keyword_overlap(self, base, compare):
        """Compute the keyword similarity between the sample answer and the user answer"""
        regex = r'\b\w+\b'
        base_words = set(re.findall(regex, self.normalize(base)))
        compare_words = set(re.findall(regex, self.normalize(compare)))
        intersection = base_words & compare_words
        union = base_words | compare_words
        return round((len(intersection) / max(len(union), 1)) * 100, 2)
    
    def compute_final_score(self, base, compare):
        """Compute the overall similarity between the sample answer and the user answer"""
        if self.is_gibberish(compare):
            return 0.0
        semantic_score = self.compute_semantic_similarity(base, compare)
        keyword_score = self.compute_keyword_overlap(base, compare)
        final_score = (0.6 * semantic_score) + (0.25 * keyword_score)
        if self.is_one_line(compare):
            final_score -= 5
        if self.is_incomplete(compare):
            final_score -= 7.5
        if self.is_wrong_answer(semantic_score):
            final_score -= 20
        final_score = max(0.0, min(100.0, round(final_score, 2)))
        return final_score
