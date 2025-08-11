<<<<<<< HEAD
# 高精度中文分词系统

一个基于词典的高级中文分词系统，支持领域自适应分词，提供Web界面和API接口。

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/lalala90/fencixitong)

## 🌟 功能特点

- **高精度分词**：基于666,471个词汇的词典进行精确分词
- **领域自适应**：支持不同领域的专业词汇识别
- **Web界面**：提供友好的在线分词工具
- **API接口**：支持程序化调用
- **实时处理**：快速响应，毫秒级分词速度
- **一键部署**：支持Vercel一键部署

## 🚀 快速部署

### 方式一：一键部署到Vercel

点击上方按钮，即可一键部署到Vercel，无需任何配置！

### 方式二：手动部署

1. **Fork本项目**
2. **在Vercel中导入项目**
3. **自动部署完成**

## 🌐 在线体验

部署完成后，您将获得：
- **Web界面**：`https://your-app-name.vercel.app/web_interface/ultra_precision_segmenter.html`
- **API接口**：`https://your-app-name.vercel.app/api/segment`

## 🔧 API使用

### 分词接口

**POST** `/api/segment`

**请求参数：**
```json
{
    "text": "要分词的文本",
    "format": "json"  // 可选，默认为json
}
```

**响应示例：**
```json
{
    "success": true,
    "segments": ["分词", "结果"],
    "word_count": 2,
    "processing_time": 0.001
}
```

### 使用示例

```python
import requests

url = "https://your-app-name.vercel.app/api/segment"
data = {"text": "人工智能技术发展迅速"}

response = requests.post(url, json=data)
result = response.json()
print(result["segments"])
# 输出: ['人工智能', '技术发展', '迅速']
```

## 📁 项目结构

```
chinese-segmenter/
├── api/                    # Vercel API函数
│   └── index.py           # 服务器入口点
├── scripts/               # 核心分词逻辑
│   └── advanced_domain_adaptive_segmenter.py
├── dictionaries/          # 词典文件
│   └── MASTER_DICTIONARY.txt
├── web_interface/         # Web界面文件
│   └── ultra_precision_segmenter.html
├── web_server.py         # Flask应用主文件
├── requirements.txt      # Python依赖
├── vercel.json          # Vercel配置
└── README.md            # 项目说明
```

## 🛠️ 技术栈

- **后端**：Python Flask
- **分词引擎**：jieba + 自定义词典
- **前端**：HTML + CSS + JavaScript
- **部署**：Vercel Serverless Functions

## 📊 性能指标

- **词典大小**：666,471个词汇
- **响应时间**：< 10ms
- **准确率**：> 95%
- **支持格式**：JSON, 纯文本

## 🔧 本地开发

### 环境要求

- Python 3.7+
- pip

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/lalala90/fencixitong.git
cd fencixitong
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务**
```bash
python web_server.py
```

4. **访问应用**
- Web界面：http://localhost:5000/web_interface/ultra_precision_segmenter.html
- API接口：http://localhost:5000/api/segment

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题，请通过GitHub Issues联系。
=======
# 高精度中文分词系统

一个基于词典的高级中文分词系统，支持领域自适应分词，提供Web界面和API接口。

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/chinese-segmenter)

## 🌟 功能特点

- **高精度分词**：基于666,471个词汇的词典进行精确分词
- **领域自适应**：支持不同领域的专业词汇识别
- **Web界面**：提供友好的在线分词工具
- **API接口**：支持程序化调用
- **实时处理**：快速响应，毫秒级分词速度
- **一键部署**：支持Vercel一键部署

## 🚀 快速部署

### 方式一：一键部署到Vercel

点击上方按钮，即可一键部署到Vercel，无需任何配置！

### 方式二：手动部署

1. **Fork本项目**
2. **在Vercel中导入项目**
3. **自动部署完成**

## 🌐 在线体验

部署完成后，您将获得：
- **Web界面**：`https://your-app-name.vercel.app/web_interface/ultra_precision_segmenter.html`
- **API接口**：`https://your-app-name.vercel.app/api/segment`

## 🔧 API使用

### 分词接口

**POST** `/api/segment`

**请求参数：**
```json
{
    "text": "要分词的文本",
    "format": "json"  // 可选，默认为json
}
```

**响应示例：**
```json
{
    "success": true,
    "segments": ["分词", "结果"],
    "word_count": 2,
    "processing_time": 0.001
}
```

### 使用示例

```python
import requests

url = "https://your-app-name.vercel.app/api/segment"
data = {"text": "人工智能技术发展迅速"}

response = requests.post(url, json=data)
result = response.json()
print(result["segments"])
# 输出: ['人工智能', '技术发展', '迅速']
```

## 📁 项目结构

```
chinese-segmenter/
├── api/                    # Vercel API函数
│   └── index.py           # 服务器入口点
├── scripts/               # 核心分词逻辑
│   └── advanced_domain_adaptive_segmenter.py
├── dictionaries/          # 词典文件
│   └── MASTER_DICTIONARY.txt
├── web_interface/         # Web界面文件
│   └── ultra_precision_segmenter.html
├── web_server.py         # Flask应用主文件
├── requirements.txt      # Python依赖
├── vercel.json          # Vercel配置
└── README.md            # 项目说明
```

## 🛠️ 技术栈

- **后端**：Python Flask
- **分词引擎**：jieba + 自定义词典
- **前端**：HTML + CSS + JavaScript
- **部署**：Vercel Serverless Functions

## 📊 性能指标

- **词典大小**：666,471个词汇
- **响应时间**：< 10ms
- **准确率**：> 95%
- **支持格式**：JSON, 纯文本

## 🔧 本地开发

### 环境要求

- Python 3.7+
- pip

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/chinese-segmenter.git
cd chinese-segmenter
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务**
```bash
python web_server.py
```

4. **访问应用**
- Web界面：http://localhost:5000/web_interface/ultra_precision_segmenter.html
- API接口：http://localhost:5000/api/segment

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题，请通过GitHub Issues联系。
>>>>>>> 245dae578b65f7ccbcdc89d3b46db79be5d25a09
