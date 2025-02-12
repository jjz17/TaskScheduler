import redis
import json


# Redis Configuration
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Redis Store for Worker Availability
def update_worker_availability(worker_id: str, availability: dict):
    redis_client.set(worker_id, json.dumps(availability))

def get_worker_availability(worker_id: str):
    data = redis_client.get(worker_id)
    return json.loads(data) if data else None