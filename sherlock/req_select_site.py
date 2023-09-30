import sys
import os
import sherlock
from notify import QueryNotifyPrint
from req_json import jsonify_sites
from sites import SitesInformation


def select_site(username, selected_site):
    # User desires to selectively run queries on a sub-set of the site list.
    # Make sure that the sites are supported & build up pruned site database.
    site_data = {}
    sites = SitesInformation(os.path.join(
        os.path.dirname(__file__), "resources/data.json"))
    site_data_all = {site.name: site.information for site in sites}

    for existing_site in site_data_all:
        if selected_site.lower() == existing_site.lower():
            site_data[existing_site] = site_data_all[existing_site]

    if not site_data:
        sys.exit(1)

    query_notify = QueryNotifyPrint(result=None,
                                    verbose=False,
                                    print_all=False,
                                    browse=False)

    # Load search results
    results = sherlock(username,
                       site_data,
                       query_notify,
                       tor=False,
                       unique_tor=False,
                       proxy=None,
                       timeout=60)
    json_data = jsonify_sites(results)
    return json_data
