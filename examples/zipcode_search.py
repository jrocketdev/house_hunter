from house_hunter.redfin.utils import find_redfin_region_by_search_string
from house_hunter.redfin.listing_search import RedfinListingSearch

zip_codes = ['92115', '92105']
all_results = []
for zip_code in zip_codes:
    location_results = find_redfin_region_by_search_string(zip_code)

    # Assume it's the first index (safe bet)
    chosen_location = location_results[0]
    id_string = chosen_location['id']

    results = RedfinListingSearch.do_search_by_id_str(region_str=id_string)
    print(f'Number of houses for {zip_code} was {len(results)}')
    all_results += results

print(f'Total number of properties is {len(all_results)}')

print('Now lets only list them if they are above 1500sqft and 3 beds and 2 baths and one room >= 14x12')
meet_criteria = []

for res in all_results:
    if res.house.square_footage <= 0 or res.house.num_bathrooms == 0 or res.house.num_bedrooms == 0:
        res.populate_details()
    if res.house.num_bedrooms >= 3 \
        and res.house.num_bathrooms >= 2 \
        and res.house.square_footage >= 1500 \
        and res.house.list_price <= 550000:
        res.populate_details()

        for bedroom in res.house.bedrooms:
            if bedroom.square_footage >= 14.0*12.0:
                meet_criteria.append(res)
                break

print('')
print('Meets Criteria: ')
for res in meet_criteria:
    print(res.house)
print(len(meet_criteria))
