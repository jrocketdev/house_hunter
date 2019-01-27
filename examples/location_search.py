from house_hunter.redfin.utils import RedfinLocationSearch

# results = RedfinLocationSearch.do_search('San Diego, CA')
location_results = RedfinLocationSearch.do_search('92115')

for res in location_results:
    print(res)

chosen_index = 0
chosen_location = location_results[chosen_index]
id_string = res['id']

from house_hunter.redfin.listing_search import RedfinListingSearch

results = RedfinListingSearch.do_search_by_id_str(region_str=id_string)
print(len(results))

# results = RedfinLocationSearch.do_search('606 Third Ave, San Diego, CA', is_addr=True)
# for res in results:
#     print(res)
