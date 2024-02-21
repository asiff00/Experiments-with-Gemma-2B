from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "google/gemma-2b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def generate_answers(query):
    input_ids = tokenizer(query, return_tensors="pt")
    output = model.generate(**input_ids)
    return tokenizer.decode(output[0])
