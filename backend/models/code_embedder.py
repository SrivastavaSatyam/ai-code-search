from transformers import AutoTokenizer, AutoModel
import torch
from typing import List, Union
import numpy as np
from config import settings

class CodeEmbedder:
    def __init__(self):
        self.device = torch.device(settings.DEVICE)
        print(settings.MODEL_NAME, type(settings.MODEL_NAME))

        self.tokenizer = AutoTokenizer.from_pretrained(str(settings.MODEL_NAME))
        self.model = AutoModel.from_pretrained(settings.MODEL_NAME).to(self.device)
        self.model.eval()

    def get_embeddings(self, code_snippets: Union[str, List[str]]) -> np.ndarray:
        if isinstance(code_snippets, str):
            code_snippets = [code_snippets]
            
        inputs = self.tokenizer(
            code_snippets,
            padding=True,
            truncation=True,
            max_length=settings.MAX_SEQUENCE_LENGTH,
            return_tensors="pt"
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
            
        return embeddings.cpu().numpy() 