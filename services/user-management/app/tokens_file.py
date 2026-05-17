from datetime import datetime, timedelta
from jose import jwt
import uuid

from elasticshearch_file import elasic_instance

import os
SECRET_KEY = os.environ.get("SECRET_KEY")

def find_user_by_email(email):
    try:
        result = elasic_instance.es.search(index="users", body={"query": {"term": {"email.keyword": email}}})
        hits = result["hits"]["hits"]
        if hits:
            return hits[0]["_id"], hits[0]["_source"]
        else:
            return None, None
    except Exception as err:
        print(err)
        return None, None

def make_token(user_id):
    expire = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode({"sub":user_id, "exp": expire}, SECRET_KEY, algorithm="HS256")

def get_user_id_from_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except Exception as err:
        print(err)
        return None

def get_user_by_id(id):
    try:
        result = elasic_instance.es.get(index="users",id=id)
        user = result["_source"]
        return user
    except:
        return None