# Known entity fetcher from Wikidata

import json
import requests
import marisa_trie
import sys

try:
	import requests_cache
	requests_cache.install_cache('wikidata_cache')
except:
	print("Couldn't find requests_cache\nIt's a good idea to install requests cache when experimenting")


SPARQL_QUERY = """
SELECT ?subj ?label
WHERE
{{
	?subj {determiner} {property} .
	SERVICE wikibase:label {{
		bd:serviceParam wikibase:language "en" .
		?subj rdfs:label ?label .
	}}
}}
GROUP BY ?subj ?label
"""

# A better query would actually be
# P106\wdt:P279* wd:Q639669 which would find all
# entities with occupation musician OR subclasses of musician
# however, it times out on the server and it doesn't allow for 
# fine-grained control so currently all occupations / band types 
# are queried seperately

URL = "https://query.wikidata.org/sparql?query={SPARQL}&format=json"

def query(det, prop):
	query = SPARQL_QUERY.format(determiner=det, property=prop)
	result = requests.get(URL.format(SPARQL=query))
	j = result.json()
	return j

def gather_results(queries):
	keys, values = [], []
	for q in queries:
		print(q)
		j = query(q[0], q[1])

		for elem in j['results']['bindings']:
			print(elem)
			keys.append(elem['label']['value'].lower())
			values.append((int(elem['subj']['value'].split('/')[-1][1:]), ))

	return keys, values

def build_dictionary():
	keys, values = gather_results([
		('wdt:P31', 'wd:Q215380'), # bands
		('wdt:P106', 'wd:Q639669'), # musicians
		('wdt:P106', 'wd:Q2252262'), # rapper
		('wdt:P106', 'wd:Q177220'), # singer
		('wdt:P106', 'wd:Q488205'), # singer-songwriter
		('wdt:P31', 'wd:Q2491498'), # pop group
		('wdt:P31', 'wd:Q2596245'), # jazz band
		('wdt:P31', 'wd:Q5741069'), # rock band
		('wdt:P31', 'wd:Q7628270'), # studio band
		('wdt:P31', 'wd:Q19464263'), # hip hop group
		('wdt:P31', 'wd:Q109940'), # duet
	])
	trie =  marisa_trie.RecordTrie('<L', zip(keys, values))

	with open('data_music.marisa', 'w') as f:
		trie.write(f)

def lookup_dictionary(word):
	trie =  marisa_trie.RecordTrie('<L')
	trie.load('data_music.marisa')
	if trie.get(word):
		print("Found {}\n  Wikidata ID: {}".format(word, trie.get(word)))
	else:
		print("Unfortunately not indexed")
	if trie.items(word):
		print("The following partial matches are available:")
		for i in trie.items(word):
			print(i)

if __name__ == '__main__':
	if not len(sys.argv) > 1:
		build_dictionary()
	else:
		lookup_dictionary(sys.argv[1])