#elasticsearch python file
from elasticsearch import Elasticsearch
import os
from pathlib import Path
import glob 
import re 
import json
from collections import namedtuple
import csv 


es = Elasticsearch('http://localhost:9200')

ParsedFilename = namedtuple('ParsedFilename', ['filename', 'is_city', 'place_name', 'plan_date', 'filetype'])
def parse_filename(filename):
	"""
	assumes filename is valid 
	filename format expected is CA_City-Rolling-Hills-Estates_2014.txt
	"""
	search_result = re.search(r'([A-z]{2})_(City|county)-([A-z-]*)_([0-9]{4}|nd).(txt|pdf|PDF.txt)', filename)
	print(filename)
	assert search_result, 'invalid filename, must follow format State_CityORcounty_Place-Name_PlanYear.filetype'

	state = search_result.group(1)
	is_city = True if search_result.group(2) == 'City' else False
	place_name = re.sub('-',' ', search_result.group(3))
	plan_date = search_result.group(4)
	filetype = search_result.group(5)

	return {'state': state, 'filename': filename,'is_city': is_city,'place_name': place_name, 'plan_date': plan_date, 'filetype': filetype}

county_dict = None
city_dict = None 
def build_pop_dicts():
	global county_dict
	global city_dict
	data_dir = os.path.join('static', 'data') 
	dict_dict = {}
	for filename in ['cityPopulations.csv', 'countyPopulations.csv']:
		file_dir = os.path.join(data_dir, filename)
		my_dict = {}
		with open(file_dir) as csvfile:
			r = csv.reader(csvfile)
			for row in r:
				my_dict[row[0]] = row[1:]
		dict_dict[filename] = my_dict
	county_dict = dict_dict['countyPopulations.csv']
	city_dict = dict_dict['cityPopulations.csv'] 	

def get_place_properties(is_city, place_name):
	if county_dict is None or city_dict is None:
		build_pop_dicts()
	if is_city:
		return city_dict[place_name]
	else:
		return county_dict[place_name]


def index_everything():
	global es
	wd = os.getcwd()
	data_dir = os.path.join(wd, 'static', 'data', 'places')
	print(data_dir)
	filepaths = glob.glob(data_dir+'/*.txt')
	hash_to_prop_mapping = {}
	i = 0 
	for filepath in filepaths:
		try: 
			filename = os.path.basename(filepath)
			parsed_filename = parse_filename(filename)
			txt = Path(filepath).read_text()
			txt = re.sub(r'\s+', ' ', txt).lower()
		except Exception as e:
			print(f'issue with filepath {filepath}')
			print(e)
			continue 
		
		keyhash = i
		hash_to_prop_mapping[keyhash] = parsed_filename
		es.index(index='test_3', id=keyhash, body={'text': txt, 'plan_filename': filename})
		i += 1

	with open('key_hash_mapping.json', 'w') as fp:
		json.dump(hash_to_prop_mapping, fp)
		print(hash_to_prop_mapping)

def search_contains_phrase(words):
	global es
	search = es.search(index='test_3', body={'query': {'match_phrase': {'text': words.lower()}}})
	ids = []
	for hit in search['hits']['hits']:
		ids.append(int(hit['_id']))

	ids = [int(hit['_id']) for hit in search['hits']['hits']]
	return ids , search['hits']['total']['value']


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
index_to_info_map = None
def map_keys_to_values(search_result_indices, key_to_hash_path='key_hash_mapping.json'):
	global index_to_info_map
	if index_to_info_map is None:
		with open(key_to_hash_path, 'r') as fp:
			data = json.load(fp)
			my_dict = data
			index_to_info_map = my_dict
	else:
		my_dict = index_to_info_map

	return list(map(lambda x:my_dict[str(x)]['filename'], search_result_indices))

def map_index_to_vals(search_result_indices, key_to_hash_path='key_hash_mapping.json'):
	global index_to_info_map
	if index_to_info_map is None:
		with open(key_to_hash_path, 'r') as fp:
			data = json.load(fp)
			my_dict = data
			index_to_info_map = my_dict
	else:
		my_dict = index_to_info_map

	return list(map(lambda x:my_dict[str(x)], search_result_indices))




if __name__ == "__main__":
	# index_everything()
	search_result_indices, hits = search_contains_phrase('fruit stands')
	print(search_result_indices)
	print(hits)
	# result = map_keys_to_values(search_result_indices)
	# print(result)
	# build_pop_dicts()

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


