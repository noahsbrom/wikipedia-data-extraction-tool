# Wikipedia Infobox Inferencing
This tool consists of a basic Flask frontend that allows the user
to insert a single Wikipedia url. The url is passed to the backend, 
where I use the Gemini LLM from Google Cloud to infer the
article's infobox information based on its text. 

### Deploying the app
`deploy.sh` is a bash script that automatically runs the Flask 
application. It deploys the app in a virtual environment that isolates
project dependencies. Since I am using a cloud-based solution, access is not public (for cost concerns). 

### Evaluation Metric
I used a metric similar to Jaccard similarity, which evaluates the similarity of two sets. Given two sets A and B, the Jaccard similarity is defined as the length of their intersection divided by the length of their union: 

| A n B | / | A u B |

Instead of using the union in the denominator, I take the minimum length of sets A and B: 

| A n B | / min(|A|, |B|). 

This variation focuses more on the generated content. More importantly, it minimizes the penalty from length discrepancies between actual and generated infobox lengths. 

### Test Results
Given the 34 test Wikipedia articles in `test_wiki_urls.txt`, I obtained 
a similarity score of 0.366 between the actual and generated infoboxes. The seemingly low score is a result of various factors:

- Some infoboxes contain information not included in the article. For example, sometimes birth date is only shown in the infobox
- Exact matches can be tricky. For example, the expected infobox might say 'Born: 1970', but the generated infobox might say 'Birth Date: 1970'
- LLM is not fine-tuned for this specific use-case

### Other Models
I attempted to solve this problem using other LLMs, specifically GPT-2 
and LLama 2 (7b). Both versions were highly inaccurate, and Llama 2
was incredibly slow. 




