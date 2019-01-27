from house_hunter.redfin_hunter import RedfinListingSearch

region_str = '2_16904'

results = RedfinListingSearch.do_search_by_id_str(region_str=region_str)
print(results[0])
print(len(results))
