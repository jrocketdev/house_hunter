from house_hunter.redfin_hunter import RedfinLocationSearch

results = RedfinLocationSearch.do_search('San Diego, CA')

for res in results:
    print(res)

results = RedfinLocationSearch.do_search('606 Third Ave, San Diego, CA', is_addr=True)

for res in results:
    print(res)
