import faiss
import numpy as np
from typing import List, Dict
from .error import LLMPException
from .embeddings_interface import EmbeddingVector

class FAISSDatabase:
    def __init__(self, embedding_type, embedding_size):
        self.embedding_type = embedding_type
        self.embedding_size = embedding_size
        self.index1 = faiss.IndexFlatL2(embedding_size)
        self.index = faiss.IndexIDMap(self.index1)

    def _handle_embedding(self, embedding:EmbeddingVector):
        ae = embedding.vector.reshape(1, -1)
        if ae.shape[1] != self.embedding_size:
            raise LLMPException.param_error(f"embedding size mismatch: {ae.shape[1]} dimensions vs {self.embedding_size} expected")
        n = np.linalg.norm(ae[0])
        if n != 0:
            ae[0] = ae[0] / n
        return ae

    @property
    def count(self):
        return self.index.ntotal

    def put_record(self, record_id, embeddings:EmbeddingVector):
        ae = self._handle_embedding(embedding)
        self.index.add_with_ids(ae, np.array([record_id], dtype=np.int64))

    def put_records(self, embeddings:Dict[int,EmbeddingVector]):
        ids = np.array([record_id for record_id in embeddings.keys()], dtype=np.int64)
        vdata = np.zeros((len(ids), self.embedding_size), dtype=np.float64)
        for i,vid in enumerate(ids):
            v = self._handle_embedding(embeddings[vid])
            vdata[i,:] = v[0]
        self.index.add_with_ids(vdata, ids)

    def delete_record(self, record_id:int):
        self.index.remove_ids(np.array([record_id], dtype=np.int64))

    def delete_records(self, record_ids:List[int]):
        self.index.remove_ids(np.array(record_ids, dtype=np.int64))

    def search(self, embedding:EmbeddingVector, max_results=5):
        ae = self._handle_embedding(embedding)
        distances, indices = self.index.search(ae, max_results)
        return zip(distances.tolist()[0], indices.tolist()[0])