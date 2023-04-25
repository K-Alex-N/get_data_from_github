import json

from app.models import Url, ParseData


def create_JSON():
    """
    название файла это pull_request.id

    data = {
        url: {
            date: {
                parse_data
            },
            next_date: {},
        next_url: {}
        }

    data = {
        "https://github.com/django/django": {
            "2023-04-25 11:10:01.535551": {
                'stars': 70048,
                'fork': 29103,
                'last_commit': "2023-04-25T07:30:52Z",
                'last_release': "2023-04-05T05:53:22Z"
            }
        }
    """

    # get data from DB
    d = {}
    urls_id = Url.query.filter_by(pull_request_id=11)
    for u in urls_id:
        d[u.id] = {}
        data_by_url_id = ParseData.query.filter_by(url_id=u.id)
        for data in data_by_url_id:
            d[u.id][data.added_at] = {
                'stars': data['stars'],
                'fork': data['fork'],
                'last_commit': data['last_commit'],
                'last_release': data['last_release'],
            }
    print(d)



    # put data into dict

    # create JSON file
    # with open("sample.json", "w") as f:
    #     json.dump(d, f)
