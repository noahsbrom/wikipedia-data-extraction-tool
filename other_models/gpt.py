import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import wiki_scrape
import time

paragraphs, infobox = wiki_scrape.main()

print('first paragraph:', paragraphs[0], '\n')

print('infobox:')
for k, v in infobox.items():
    print(f'{k}: {v}')

start = time.time()

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

query = 'generate wikipedia infobox data as key:value pairs based on the following wiki paragraph:\n' + paragraphs[0]
max_new_tokens = 20

inputs = tokenizer.encode(query, return_tensors='pt')
outputs = model.generate(inputs, do_sample=True, pad_token_id=tokenizer.eos_token_id, attention_mask=torch.ones_like(inputs), max_new_tokens=max_new_tokens)

output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
end = time.time()

print('output:', output_text)
print('execution time:', end - start, 'seconds')
