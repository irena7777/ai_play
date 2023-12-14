from openai import OpenAI

def search(search_term):
    client = OpenAI(api_key='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')

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
    return response.choices[0].message.content