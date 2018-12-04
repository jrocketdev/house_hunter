import sys
from house_hunter.house_hunter import RedfinListing

property_id = '21670371'
listing_id = '97241798'

listing = RedfinListing(property_id=property_id, listing_id=listing_id)
print(listing)

# Force listing to go collect the details
success = listing.populate_details()
if success:
    print('Successfully retrieved full listing!')
else:
    print('Unable to find full listing details... check property id and listing id?')
    sys.exit(-1)

print(listing.comprehensive_dict)