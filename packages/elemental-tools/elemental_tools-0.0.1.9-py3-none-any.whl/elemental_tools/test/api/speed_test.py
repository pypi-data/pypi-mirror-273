import time
import requests
from multiprocessing import Pool

NUM_REQUESTS = 200


def make_request(_):
    try:
        response = requests.get("http://localhost:3001/")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None


if __name__ == "__main__":
    start_time = time.time()

    with Pool() as pool:
        results = pool.map(make_request, range(NUM_REQUESTS))

    end_time = time.time()
    total_time = end_time - start_time

    successful_requests = sum(1 for result in results if result == 200)
    failed_requests = len(results) - successful_requests

    print("Total Per Sec:", NUM_REQUESTS / total_time)
    print("Total time taken:", total_time)
    print("Successful requests:", successful_requests)
    print("Failed requests:", failed_requests)
