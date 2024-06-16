from flask import Flask, jsonify, redirect, url_for
import os
import json
import random
import threading

app = Flask(__name__)

# 启动 main.py 的函数
def start_main():
    os.system('python main.py')

# 启动一个线程来运行 main.py
main_thread = threading.Thread(target=start_main)
main_thread.start()

# 处理根路径
@app.route('/')
def index():
    return "欢迎使用本程序。"

# 处理 /api/random_list/<hash_value> 路径
@app.route('/api/random_list/<hash_value>')
def get_random_list(hash_value):
    cache_dir = 'cache'
    filename = os.path.join(cache_dir, f'{hash_value}.json')

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data)
    else:
        return jsonify({"error": "未找到对应的缓存文件。"})

# 处理 /api/random/<hash_value> 路径
@app.route('/api/random/<hash_value>')
def get_random_link(hash_value):
    cache_dir = 'cache'
    filename = os.path.join(cache_dir, f'{hash_value}.json')

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data and isinstance(data, list):
                random_link = random.choice(data)
                return redirect(random_link)
            else:
                return jsonify({"error": "缓存文件内容不符合预期。"})
    else:
        return jsonify({"error": "未找到对应的缓存文件。"})

if __name__ == '__main__':
    app.run(debug=True)
