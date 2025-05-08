# coding=utf-8
# 数据库相关操作
from neo4j import GraphDatabase

NEO4J_URI="neo4j://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="" //注意：这里输入你的neo4j密码

# 建立数据库的连接
def get_db():
    db = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    db.verify_connectivity()
    return db

def close_db(db):
    db.close()

def test_query(db):
    query = '''
        MATCH (p:人物{name: $person_name})
        RETURN p.name AS name
    '''
    with db.session(database="neo4j") as session:
        result = session.run(query, person_name="陈奕迅")
        # print(result.keys())
        # res = [record["p"] for record in result]
        print(result.values("name"))
    return

if __name__ == "__main__":
    db = get_db()
    test_query(db)
    close_db(db)
    print('done')
    
