from house_hunter.house_hunter import RedfinSearch

region_str = '2_16904'

results = RedfinSearch.do_search_by_id_str(region_str=region_str)
print(results[0])
print(len(results))
