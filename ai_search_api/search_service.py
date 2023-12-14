from openai import OpenAI
import requests
from pprint import pprint as pp
import json

from ai_search_api.serializers import SearchResultsSerializer


def search(search_term):
    client = OpenAI(api_key='')

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a professional photographer. "
                                          "Given the following message, find out which piece of photographic equipment (cameras, lenses, drones and video cameras) would match the message."
                                          " Write your responses as a list of 10 product models in json called models with name of the model as name and a couple of sentences description of the model as description."},
            {"role": "user", "content": search_term}
        ]
    )

    result = json.loads(response.choices[0].message.content)
    # pp(result["models"])
    # serializer = SearchResultsSerializer(data=result["models"], many=True)
    # serializer.is_valid()
    # models = serializer.save()

    model_results_from_ss = []
    for model in result["models"]:
        results = get_from_mpb_search_service(model["name"])
        if len(results) > 0:
            result = results[0]
            result["chat_gpt_description"] = model["description"]
            model_results_from_ss.append(result)

    # search_service_results = get_from_mpb_search_service(result)
    # pp(search_service_results)

    # return response.choices[0].message.content
    return {"models": model_results_from_ss}

def get_from_mpb_search_service(model_name):
    import requests

    url = "https://www.mpb.com/search-service/product/query/?field_list=model_id&field_list=model_name&field_list=model_description&field_list=product_price.minimum&field_list=product_price.maximum&field_list=product_price.count&field_list=model_url_segment&field_list=model_available_new&filter_query[model_market]=UK&filter_query[object_type]=product&filter_query[model_available]=true&filter_query[model_is_published_out]=true&facet_field=model_brand&facet_field=model_category&facet_field=model_type&facet_field=product_condition_star_rating&facet_field=product_price&facet_field=%2A&start=0&rows=52&group_field=model_id&minimum_match=100%25"
    params = {"filter_query[model_name]": model_name}
    payload = {}
    headers = {
        'Content-Language': 'en_GB',
        'Cookie': '__cf_bm=LYKlI9RURfdxaVSNZWHN22ofAJr5ONy7F4HY41dzPF0-1702573046-1-AciOFERyTvL2hDZWtqJ321BB2eqvHpk69ROjgchVA/Io0VwkWagMCOkPJ1uGZC9f6iZ1YBnNCjHJ4Me85dNsPxM=; _cfuvid=rXj5_PxtKHNmB_NGd_bFrj10GcsXBiWCgu1ev0ywvJA-1702566297819-0-604800000'
    }

    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    json_response = response.json()

    return json_response["results"]