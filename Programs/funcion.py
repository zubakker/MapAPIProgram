def scale_for_response(json_response):
    size = json_response["properties"]["ResponseMetaData"]["SearchResponse"]["boundedBy"]
    size = size[1][0] - size[0][0], size[1][1] - size[0][1]
    return size
