
import numpy as np
from typing import List

def embed_texts(texts: List[str], dim: int = 768) -> np.ndarray:
    rng = np.random.RandomState(42)
    vecs = []
    for t in texts:
        h = abs(hash(t)) % (10**8)
        rng.seed(h)
        v = rng.rand(dim).astype("float32")
        v /= (np.linalg.norm(v) + 1e-9)
        vecs.append(v)
    return np.vstack(vecs)
