# KLPBBS Random API

这是一个可以部署到服务器，自动获取苦力怕论坛帖子数据，并进行定时缓存，提供API的工具。

## 开发进展

* [X] 自动读取url.json，热更新需要读取的分区/版块链接。
* [X] 定时自动运行，并使用Flask建立服务。
* [X] 使用 `/api/random/唯一哈希值` 来跳转到对应分区/版块的的随机一个链接中。
* [X] 使用 `/api/random_list/唯一哈希值` 查阅对应分区/版块目前缓存的链接列表。
* [ ] 使用 `/api/random_link` 查阅url.json中已添加的链接和对应的哈希值，以及目前更新配置和上次更新时间。
* [ ] 可以通过前端快速的调整服务器里面的配置。

## 项目结构

```
.
├── app.py
├── cache
├── main.py
├── read.py
└── url.json
```

### 文件说明

- `app.py`：主应用程序文件，包含 API 的主要逻辑，同时多线程启动 `main.py`。
- `cache`：缓存文件夹，用于存储临时数据。
- `main.py`：主程序，用于配置读取速率还有传输、储存缓存数据。
- `read.py`：用于读取和处理数据的脚本。
- `url.json`：包含 API 使用的 URL 配置文件。

## 环境依赖

本项目使用 Python 语言开发。运行此项目需要以下 Python 包：

- `flask`：用于创建 Web API
- `requests`：用于发送 HTTP 请求
- `beautifulsoup4`：用于解析 HTML

可以使用以下命令安装依赖：

```bash
pip install flask requests beautifulsoup4
```

## 安装和运行

1. 克隆项目到本地：

   ```bash
   git clone https://github.com/your_username/klpbbs-random-api.git
   ```
2. 进入项目目录：

   ```bash
   cd klpbbs-random-api
   ```
3. 安装依赖：

   ```bash
   pip install flask requests beautifulsoup4
   ```
4. 运行应用程序：

   ```bash
   python app.py
   ```

## 配置

- `main.py`：`time.sleep(1800)` 可以更改自动重启的时间，默认1800秒（半小时）。
- `url.json`：添加需要读取的链接列表，请遵循JSON格式规范。

## 使用说明

在启动应用程序后，你可以通过访问以下端点来使用 API：

- `/api/random/唯一哈希值`：跳转到对应分区/版块的的随机一个链接中。
- `/api/random_list/唯一哈希值`：查阅对应分区/版块目前缓存的链接列表。
- `/api/random_link`：待更新，功能见“开发进展”。

## 作者

Keishi

## 贡献

欢迎提出问题（issues）和贡献代码（pull requests）。

## 许可证

本项目采用 MIT 许可证。详细信息请参见 LICENSE 文件。
