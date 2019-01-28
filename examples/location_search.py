from house_hunter.redfin.utils import find_redfin_region_by_search_string

# results = RedfinLocationSearch.do_search('San Diego, CA')
location_results = find_redfin_region_by_search_string('92115')
for res in location_results:
    print(res)

chosen_index = 0
chosen_location = location_results[chosen_index]
id_string = res['id']

from house_hunter.redfin.listing_search import RedfinListingSearch

results = RedfinListingSearch.do_search_by_id_str(region_str=id_string)
print(len(results))

# for res in results:
#     print(res.house)

print('Now lets only list them if they are above 1500sqft and  3 beds and 2 baths')
meet_criteria = []

for res in results:
    if res.house.num_bedrooms >= 3 and res.house.num_bathrooms >= 2 and res.house.square_footage >= 1500:
        print(res.house)
        meet_criteria.append(res)
print(len(meet_criteria))
