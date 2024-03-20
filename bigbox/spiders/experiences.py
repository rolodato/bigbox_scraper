import json
from urllib.parse import urljoin, urlencode

import scrapy
from bs4 import BeautifulSoup


def get_text(s):
    soup = BeautifulSoup(s, "html.parser")
    return soup.get_text().strip()


class ExperiencesSpider(scrapy.Spider):
    name = "experiences"
    allowed_domains = ["bigbox.com.ar"]
    box_slug = "bonjour"

    def post_body(self, page_number):
        return {
            "operationName": "PaginatedBoxActivities",
            "query": "query PaginatedBoxActivities($box_slug: String!, $provinceId: ID, $page_number: Int, $order_by: String, $search_term: String, $at_home: Boolean, $per_page: Int) {\n  paginated_box_activities(box_slug: $box_slug, province_id: $provinceId, page_number: $page_number, order_by: $order_by, search_term: $search_term, at_home: $at_home, per_page: $per_page) {\n    results {\n      box_id\n      url\n      activity {\n        has_online_reservation\n        validations\n        id\n        name\n        slug\n        description\n        short_description\n        category_id\n        benefits\n        benefits_title\n        benefits_subtitle\n        know_what\n        tip\n        slug\n        special_catalog\n        product_tags {\n          id\n          slug\n          name\n          __typename\n        }\n        product_url\n        participants\n        product_image_url\n        product_url\n        price_without_discount\n        in_campaign\n        campaign_discounted_price\n        campaign_discounted_percentage\n        is_remote\n        small_print\n        activity_type\n        online_activity_duration\n        experience_affected\n        recommended_tag\n        show_affected_text\n        images {\n          id\n          image\n          __typename\n        }\n        is_new\n        ... on RatedProductInterface {\n          reviews_qty\n          rating\n          __typename\n        }\n        ... on ComboActivityType {\n          is_combo_activity\n          combo_activities_images\n          locations {\n            id\n            latitude\n            longitude\n            sublocation\n            address\n            province_id\n            phone\n            show_in_map\n            map_image\n            province {\n              id\n              name\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        ... on PartnerActivityType {\n          partner {\n            id\n            website\n            description\n            __typename\n          }\n          locations {\n            id\n            latitude\n            longitude\n            sublocation\n            address\n            province_id\n            phone\n            show_in_map\n            map_image\n            delivery_radius\n            delivery_in_all_country\n            province {\n              id\n              name\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    page_info {\n      number\n      has_next\n      count\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables": {
                "box_slug": self.box_slug,
                "page_number": page_number,
                "per_page": 12,
                "at_home": False,
                "provinceId": None,
                "search_term": "",
            },
        }

    def page(self, page_number):
        url = f"https://www.bigbox.com.ar/graphql/?operationName=PaginatedBoxActivities"
        return scrapy.Request(
            url,
            method="POST",
            body=json.dumps(self.post_body(page_number)),
            headers={
                "Accept": "*/*",
                "Content-Type": "application/json",
            },
        )

    def start_requests(self):
        return [self.page(1)]

    def parse(self, response):
        data = json.loads(response.text)["data"]["paginated_box_activities"]
        if data["page_info"]["has_next"]:
            yield self.page(data["page_info"]["number"] + 1)
        for result in data["results"]:
            for location in result["activity"]["locations"]:
                if location["province"]["name"] == "CABA":
                    [lat, lng] = [location["latitude"], location["longitude"]]
                    query = {"query": f"{lat},{lng}"}
                    yield {
                        "name": result["activity"]["name"],
                        "benefits": get_text(result["activity"]["benefits"]),
                        "location": "https://www.google.com/maps/search/?api=1&"
                        + urlencode(query),
                        "url": urljoin("https://www.bigbox.com.ar", result["url"]),
                    }
