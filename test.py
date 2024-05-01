import infobox_generation
import time

def test(): 
    urls_file = open('test_wiki_urls.txt', 'r')

    similarity_scores = []
    times = []

    for line in urls_file:
        url = line.strip()
        if 'wikipedia' not in url: 
            continue

        start = time.time()
        response, similarity_score = infobox_generation.generate_infobox(url)
        end = time.time()
        total = end - start

        # -1 indicates article with no infobox; skip it
        if similarity_score != -1 and response != '':
            similarity_scores.append(similarity_score)
            times.append(total)
            print(f'{url}: similarity score = {similarity_score}, time = {total} seconds')

    print('-' * 20)
    print('max:', max(similarity_scores))
    print('min:', min(similarity_scores))
    print('average similarity:', sum(similarity_scores) / len(similarity_scores))
    print('average time:', sum(times) / len(times), 'seconds')
    print('total time:', sum(times), 'seconds')

    urls_file.close()
          
test()