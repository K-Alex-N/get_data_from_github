from app.store.db.models_w_flsak_alchemy import Url, ParseData


def create_JSON():

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
