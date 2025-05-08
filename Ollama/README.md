# 启动指南
- 依次运行如下代码
01_get_songs.ipynb //获取歌曲名称（爬取网易云）
02_get_baike.ipynb //获取歌曲信息（爬取百度百科）
03_ollama.ipynb //利用本地模型提取三元组（需要提前下载好ollama和本地模型）
04_make_KG.ipynb //连接neo4j数据库并构建知识图谱（需要输入neo4j的密码）
- 最后运行``streamlit run app.py`` ,启动前端项目，访问地址为http://localhost:8501。