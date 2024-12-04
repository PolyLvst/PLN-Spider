import os
import json

def check_cached_ids(path:str):
    with open(path, "r") as f:
        data = json.load(f)
    for key,value in data.items():
        if os.path.exists(f"./TempImages/meteran/image_{key}.jpg"):
            data[key] = {
                    "str_pelanggan": key,
                    "status_value": "True"}
    with open(path, "w") as f:
        json.dump(data,f)

def check_cache_img_and_rumah(path_cache_ids:str, path_meteran:str, path_rumah:str):
    data_meteran = {}
    data_rumah = {}
    with open(path_cache_ids, "r") as f:
        data = json.load(f)
    for key,value in data.items():
        if os.path.exists(f"./TempImages/meteran/image_{key}.jpg"):
            data_meteran[key] = {
                "img": f"./TempImages/image_{key}.jpg",
                "status_value": "True"}
        if os.path.exists(f"./TempImages/rumah/image_{key}.jpg"):
            data_rumah[key] = {
                "img": f"./TempImages/image_{key}.jpg",
                "status_value": "True"}
    with open(path_meteran, "w") as f:
        json.dump(data_meteran, f)
    with open(path_rumah, "w") as f:
        json.dump(data_rumah, f)

def combiner(cache_img, cache_img_rumah, cache_img_rumah_samping):
    cache_meteran = f"./DataSnapshots/cache_img.json"
    data_meteran = {}
    cache_rumah = f"./DataSnapshots/cache_img_rumah.json"
    data_rumah = {}
    cache_rumah_samping = f"./DataSnapshots/cache_img_rumah_samping.json"
    data_rumah_samping = {}
    if os.path.exists(cache_meteran):
        with open(cache_meteran, "r") as f:
            data_meteran = json.load(f)
    if os.path.exists(cache_rumah):
        with open(cache_rumah, "r") as f:
            data_rumah = json.load(f)
    if os.path.exists(cache_rumah_samping):
        with open(cache_rumah_samping, "r") as f:
            data_rumah_samping = json.load(f)
    
    with open(cache_img, "r") as f:
        data_meteran_chunk = json.load(f)
    with open(cache_img_rumah, "r") as f:
        data_rumah_chunk = json.load(f)
    with open(cache_img_rumah_samping, "r") as f:
        data_rumah_samping_chunk = json.load(f)
    
    for key, value in data_meteran_chunk.items():
        data_meteran[key] = value
    for key, value in data_rumah_chunk.items():
        data_rumah[key] = value
    for key, value in data_rumah_samping_chunk.items():
        data_rumah[key] = value
    
    with open(cache_meteran, "w") as f:
        json.dump(data_meteran, f)
    with open(cache_rumah, "w") as f:
        json.dump(data_rumah, f)
    with open(cache_rumah_samping, "w") as f:
        json.dump(data_rumah_samping, f)
    
    print("Rechunked ...")

if __name__ == "__main__":
    # for profile_num in range(1,5):
    #     check_cached_ids(f"./DataSnapshots/cached_ids_{profile_num}.json")
    # for profile_num in range(1,5):
    #     check_cache_img_and_rumah(
    #         f"./DataSnapshots/cached_ids_{profile_num}.json",
    #         f"./DataSnapshots/cache_img_{profile_num}.json",
    #         f"./DataSnapshots/cache_img_rumah_{profile_num}.json")
    for profile_num in range(1,5):
        combiner(f"./DataSnapshots/cache_img_{profile_num}.json",
                f"./DataSnapshots/cache_img_rumah_{profile_num}.json",
                f"./DataSnapshots/cache_img_rumah_samping_{profile_num}.json")