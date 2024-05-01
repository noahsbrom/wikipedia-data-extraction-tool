import google.generativeai as genai
import os
import wiki_scrape


"""
Fetch the given wikipedia url, extract its actual infoboxes,
generate a sample infobox based on the article text, then calculate
the similarity score between the two. Return the generated infobox and
the similarity score.

Return '', -1 if the article has no infoboxes
"""
def generate_infobox(url): 
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    genai.configure(api_key=google_api_key)

    paragraphs, infobox_dict = wiki_scrape.scrape_article(url)
    if infobox_dict == {}:
        return '', -1


    prompt = (
        'Generate wikipedia infobox data as key:value pairs based on the following wikipedia article. '
        'Separate each infobox pair with a new line. '
        'For example: key1:value1\nkey2:value2\n\n' + '\n'.join(paragraphs)
    )

    response = generate_text(prompt)
    if response == '':
        return '', -1
    
    similarity_score = calculate_similarity(infobox_dict, response)
    return response, similarity_score
    

"""
Use Google's Gemini LLM to generate a sample infobox based on the given article.
"""
def generate_text(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    try:
        return response.text
    except:
        return ''


""" 
This metric is similar to Jaccard similarity. Let A be the expected infobox set and B be the generated infobox
set. Then, instead of using len(A & B) / len(A | B), we use len(A & B) / len(min_len(A, B)). I did this for 
two reasons: I wanted to focus on the generated content and avoid penalties for difference in actual/generated 
infobox lengths. 
"""
def calculate_similarity(infobox_dict, response):
    key_set = set(' '.join(infobox_dict.keys()).split())
    value_set = set(' '.join(infobox_dict.values()).split())
    ib_set = key_set.union(value_set)

    response_set = set(response.split())
    response_set = set([s.lower() for s in response_set])

    intersection = ib_set.intersection(response_set)

     # minimize penalty for responses over or under the expected length
    return len(intersection) / min(len(response_set), len(ib_set))