import os
import json
import hashlib
import subprocess
import time

def read_urls_from_file():
    try:
        with open('url.json', 'r', encoding='utf-8') as f:
            urls = json.load(f)
            return urls
    except FileNotFoundError:
        print("没有找到url.json文件，请往文件里填写链接再重新启动程序。")
        exit(1)

def get_hash_from_url(url):
    # 对整个URL进行哈希值计算
    hash_value = hashlib.md5(url.encode('utf-8')).hexdigest()
    return hash_value

def run_read_py(url):
    # 调用read.py读取URL，并返回结果
    try:
        result = subprocess.check_output(['python', 'read.py', url], timeout=30)
        return result.decode('utf-8').strip().splitlines()
    except subprocess.TimeoutExpired:
        print(f"读取 {url} 超时")
        return None
    except subprocess.CalledProcessError as e:
        print(f"读取 {url} 失败: {e}")
        return None

def save_to_cache(hash_value, data):
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    filename = os.path.join(cache_dir, f'{hash_value}.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cleanup_cache(urls):
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        return
    
    cached_files = os.listdir(cache_dir)
    for filename in cached_files:
        url_hash = filename.split('.')[0]
        if url_hash not in urls:
            os.remove(os.path.join(cache_dir, filename))

if __name__ == "__main__":
    urls = read_urls_from_file()

    while True:
        for url in urls:
            print(f"正在处理 {url}...")
            result = run_read_py(url)
            if result:
                url_hash = get_hash_from_url(url)
                save_to_cache(url_hash, result)
            time.sleep(5)  # 每处理完一个URL后休眠5秒

        cleanup_cache(set(map(get_hash_from_url, urls)))  # 清理不需要的缓存文件

        # 休眠60秒后再次读取url.json进行处理
        time.sleep(1800)
