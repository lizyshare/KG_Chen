# coding=utf-8
from db import get_db, close_db
import re

patterns = [
  # 8种模式
  '歌曲(.+)所属的专辑是',
  '歌曲(.+)的歌手是',
  '歌曲(.+)的作词人是',
  '歌曲(.+)的作曲人是',
  '专辑(.+)包含的歌曲有',
  '(.+)演唱的歌曲有',
  '(.+)作词的歌曲有',
  '(.+)作曲的歌曲有',
]

queries = [
  "MATCH (a:歌曲{name:$val})-[:专辑]->(b:专辑) RETURN b.name AS name LIMIT 1",
  "MATCH (a:歌曲{name:$val})-[:歌手]->(b:人物) RETURN b.name AS name LIMIT 1",
  "MATCH (a:歌曲{name:$val})-[:作词]->(b:人物) RETURN b.name AS name LIMIT 1",
  "MATCH (a:歌曲{name:$val})-[:作曲]->(b:人物) RETURN b.name AS name LIMIT 1",
  "MATCH (a:专辑{name:$val})<-[:专辑]-(b:歌曲) RETURN b.name AS name",
  "MATCH (a:人物{name:$val})<-[:歌手]-(b:歌曲) RETURN b.name AS name LIMIT 10",
  "MATCH (a:人物{name:$val})<-[:作词]->(b:歌曲) RETURN b.name AS name LIMIT 10",
  "MATCH (a:人物{name:$val})<-[:作曲]->(b:歌曲) RETURN b.name AS name LIMIT 10",
]

def query_handler(question):
  print("问题：", question)
  for index, pattern in enumerate(patterns):
    matchObj = re.match(pattern, question)
    if matchObj:
      print("匹配成功 pattern is: ", pattern)
      val = matchObj.group(1)
      query = queries[index]
      # 查询数据库
      db = get_db()
      with db.session(database="neo4j") as session:
        result = session.run(query, val=val)
        rows = result.values('name')
        rows = [row[0] for row in rows]
        print("查询结果：", rows)
      close_db(db)
      return {
        "state": 0,
        "data": rows,
        "msg": "查询成功"
      }
  # 没有匹配的pattern
  print("匹配失败")
  return {
    "state": 1,
    "msg": "查询失败，请按照'参考模板'输入查询语句"
  }

if __name__ == "__main__":
  query_handler('歌曲相信你的人所属的专辑是')
  # query_handler('歌曲相信你的人的作词人是')
  # query_handler('歌曲相信你的人的作词人是')
  # query_handler('歌曲相信你的人的歌手是')
  # query_handler('专辑L.O.V.E.包含的歌曲有')
  # query_handler('陈奕迅演唱的歌曲有')
  # query_handler('林家谦作曲的歌曲有')
  # query_handler('小克作词的歌曲有')