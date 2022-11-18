from bs4 import BeautifulSoup


def parse_html(article_body_html):
    soup = BeautifulSoup(article_body_html)
    text = soup.get_text()
    return text

from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

def get_question(answer, context, max_length=64):
  input_text = "answer: %s  context: %s " % (answer, context)
  features = tokenizer([input_text], return_tensors='pt')

  output = model.generate(input_ids=features['input_ids'],
               attention_mask=features['attention_mask'],
               max_length=max_length)

  return tokenizer.decode(output[0])


def get_comprehension_question(article_body_html, answer):
    article_text = parse_html(article_body_html)
    answer = answer.lower()

    sentences = [sentence.strip() + '.' for sentence in article_text.split('.') if answer in sentence.lower()]
    if len(sentences) == 0:
        return None, None

    question = get_question(" ".join(sentences), answer)
    question = question.split("question:")[-1].replace("</s>", "").strip()
    return question, answer