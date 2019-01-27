from house_hunter.redfin.listing_search import RedfinListingSearch

region_str = '2_16904'  # Get the region string from?

results = RedfinListingSearch.do_search_by_id_str(region_str=region_str)
print(results[0])
print(len(results))
