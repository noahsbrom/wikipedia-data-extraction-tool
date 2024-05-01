import torch
import transformers
from transformers import LlamaForCausalLM, LlamaTokenizer, GPT2Tokenizer, GPT2LMHeadModel
import wiki_scrape
import time

paragraphs, infobox = wiki_scrape.main()
paragraphs = ' '.join([p for p in paragraphs])
start = time.time()

model_dir = '../llama/llama-2-7b-hf'
model = LlamaForCausalLM.from_pretrained(model_dir)
tokenizer = LlamaTokenizer.from_pretrained(model_dir)

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto"
)

query = 'generate wikipedia infobox data as key:value pairs based on the following wiki paragraph:\n' + paragraphs + '\n'

sequences = pipeline(
    query,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=9000
)


for seq in sequences:
    print(f"{seq['generated_text']}")

end = time.time()
print('execution time:', end - start, 'seconds')