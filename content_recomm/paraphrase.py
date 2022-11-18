from parrot import Parrot
import warnings
warnings.filterwarnings("ignore")


def load_paraphrase_model(use_gpu=True):
    parrot_model = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=use_gpu)
    return parrot_model

def get_paraphrases(parrot_model, phrases):
    print(phrases)
    for phrase in phrases:
        para_phrases = parrot_model.augment(input_phrase=phrase)
    return para_phrases

