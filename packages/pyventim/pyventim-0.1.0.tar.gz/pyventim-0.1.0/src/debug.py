# pylint: skip-file

import json
import pprint
import os
import datetime
import requests

import pyventim.public as public
import pyventim.utils as utils


def main():
    exp = public.EventimExploration()
    search_parameter = "Disneys DER KÖNIG DER LÖWEN"
    # search_parameter = "The"
    categories = ["Musical & Show|Musical"]
    city_ids = [7]  # No clue how to resolve # 7 == hamburg
    days = 7
    sort = "DateAsc"
    in_stock = True

    date_from = datetime.date.today()
    date_to = date_from + datetime.timedelta(days=days)

    time_from = datetime.time(18, 0, 0)
    time_to = datetime.time(19, 00, 00)

    print(
        "Starting search with:",
        search_parameter,
        categories,
        date_from,
        date_to,
        sort,
        in_stock,
        sep="\n  - ",
    )

    print("Explore productGroups")
    product_groups = exp.explore_product_groups(
        search_term=search_parameter,
        categories=categories,
        # date_from=date_from,
        date_to=date_to,
        time_from=time_from,
        time_to=time_to,
        city_ids=city_ids,
        page=1,
        sort=sort,
        in_stock=in_stock,
    )
    with open("./temp/product_groups.json", "w", encoding="utf-8") as f:
        json.dump(product_groups, f, indent=2)

    print("Explore attractions")
    attractions = exp.explore_attractions(search_term=search_parameter, sort=sort)
    with open("./temp/attractions.json", "w", encoding="utf-8") as f:
        json.dump(attractions, f, indent=2)

    print("Explore content")
    content = exp.explore_content(search_term=search_parameter)
    with open("./temp/content.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)

    print("Explore locations")
    locations = exp.explore_locations(search_term="Stage", page=1, sort=sort)
    with open("./temp/locations.json", "w", encoding="utf-8") as f:
        json.dump(locations, f, indent=2)


if __name__ == "__main__":
    main()
