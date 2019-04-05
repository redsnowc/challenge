import sys
import pymongo


def get_rank(user_id):
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.shiyanlou
    contests = db.contests
    data = list(contests.aggregate([
        {"$group": {"_id": "$user_id", "score": {
            "$sum": "$score"}, "time": {"$sum": "$submit_time"}}},
        {"$sort": {"score": -1, "time": 1}}]))
    for i in data:
        if i['_id'] == user_id:
            result = i

    try:
        rank = data.index(result) + 1
    except UnboundLocalError:
        print("User ID: %s does not exit." % user_id)
        sys.exit()
    score = result['score']
    submit_time = result['time']
    return rank, score, submit_time


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Parameter Error")
    else:
        try:
            user_id = int(sys.argv[1])
            print(get_rank(user_id))
        except ValueError:
            print("Parameter Error")
            sys.exit()
