#elasticsearch python file
from elasticsearch import Elasticsearch
import os
from pathlib import Path
import glob 
import re 
import json

def index_everything():
	es = Elasticsearch('http://localhost:9200')
	wd = os.getcwd()
	data_dir = os.path.join(wd, 'static', 'data', 'places')
	print(data_dir)
	filepaths = glob.glob(data_dir+'/*.txt')
	key_hash_mapping = {}
	i = 0 
	for filepath in filepaths:
		try: 
			txt = Path(filepath).read_text()
			txt = re.sub(r'\s+', ' ', txt).lower()
		except Exception as e:
			print(f'issue with filepath {filepath}')
			print(e)
			continue 
		key = os.path.basename(filepath)
		keyhash = i
		print(key, keyhash)
		key_hash_mapping[keyhash] = key
		es.index(index='test_3', id=keyhash, body={'text': txt, 'plan_name': key})
		i += 1

	with open('key_hash_mapping.json', 'w') as fp:
		json.dump(key_hash_mapping, fp)
		print(key_hash_mapping)

def search_contains_phrase(words):
	es = Elasticsearch('http://localhost:9200')
	search = es.search(index='test_3', body={'query': {'match_phrase': {'text': words.lower()}}})
	ids = []
	for hit in search['hits']['hits']:
		ids.append(int(hit['_id']))

	ids = [int(hit['_id']) for hit in search['hits']['hits']]
	return ids , search['hits']['total']['value'], 


# def my_search(query):

# 	phrase_list=re.findall(r'\"(.+?)\"',query)
# 	words_list = query.split('"')
# 	if not words_list:
# 		cw_ids = None
# 	else:
# 		cw_ids, _ = search_contains_words(' '.join(words_list))
	
# 	phrase_ids = cw_ids	
# 	for phrase in phrase_list:
# 		ids, _ = search_contains_phrase(phrase)
# 		if phrase_ids is not None:
# 			phrase_ids = list(set(phrase_ids) & set(ids))
# 		else:
# 			phrase_ids = ids
# 	print("word_list", words_list)
# 	print("phrase_list", phrase_list)

# 	return phrase_ids
key_to_hash_map = None
def map_keys_to_values(search_result_indices, key_to_hash_path='key_hash_mapping.json'):
	global key_to_hash_map
	if key_to_hash_map is None:
		with open(key_to_hash_path, 'r') as fp:
			data = json.load(fp)
			my_dict = data
			key_to_hash_map = my_dict
	else:
		my_dict = key_to_hash_map

	return list(map(lambda x:my_dict[str(x)], search_result_indices))




if __name__ == "__main__":
	index_everything()
	search_result_indices, hits = search_contains_phrase('fruit stands')
	result = map_keys_to_values(search_result_indices)
	print(result)

""""
1. implement quote detection for multiphrase search x 
2. otherwise do single phrase search x 
0. integrate results with the website  x 
3. get it installed on the server 
3.5 integrate elastic search into server (index everything)
4. Figure out how to do multiple queries with elastic search 
5. Integrate search box with elastic search 
6. Do auto indexing 


"""


