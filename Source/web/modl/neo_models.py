from py2neo import Graph, Node, Relationship, cypher, Path
import neo4j

#LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS line CREATE (n:term{nodeid:line.id, name:line.nodename, nodeclass:line.nodeclass, property:line.propertytext})
#LOAD CSV WITH HEADERS FROM 'file:///relations.csv' AS line MATCH (n1:term{nodeid:line.node1}),(n2:term{nodeid:line.node2}) CREATE (n1)-[:rel{relation:line.relation}]->(n2)
#删除知识图谱
#MATCH (:term)-[r:rel]-(:term) delete r
#MATCH (n:term) delete n

#KGneo4j类，完成数据库的查询、修改工作
class KGneo4j():
	graph = None

	def __init__(self):
		print("创建Neo4j对象...")

	def connect_db(self):
		self.graph = Graph("http://localhost:7474", username="neo4j", password="123456")

	# 可以选择使用正则表达式
	def match_item_by_name(self, name, use_re=False):
		if use_re:  # 使用正则
			sql = "MATCH (n:term) WHERE n.name=~\".*" + name + ".*\" RETURN n;"
		else:
			sql = "MATCH (n:term{name:'" + str(name) + "' }) return n;"
		answer = self.graph.run(sql).data()

		return answer

	def match_item_by_id(self, id):
		sql = "MATCH (n:term{nodeid:'" + str(id) + "' }) return n;"
		answer = self.graph.run(sql).data()
		return answer

	def match_item_by_class(self, nodeclass, use_re=False):
		if use_re: #使用正则
			sql = "MATCH (n:term) WHERE n.nodeclass=~\"" + nodeclass + "\" RETURN n;"
		else:
			sql = "MATCH (n:term{nodeclass:'" + str(nodeclass) + "' }) return n;"
		answer = self.graph.run(sql).data()
		return answer

	def match_item_by_property(self, property, use_re=False):
		if use_re: #使用正则
			sql = "MATCH (n:term) WHERE n.properties=~\"" + property + "\" RETURN n;"
		else:
			sql = "MATCH (n:term{properties:'" + str(property) + "' }) return n;"
		answer = self.graph.run(sql).data()
		return answer

	# 根据关系的名称搜索
	def get_relation(self, relation, use_re=False):
		if use_re: #使用正则
			sql = "MATCH (e1:term)-[r:rel]-(e2:term) WHERE r.relation=~\"" +str(relation)+"\" RETURN e1,r,e2"
		else:
			sql = "MATCH (e1:term)-[r:rel]-(e2:term) WHERE r.relation=\"" +str(relation)+"\" RETURN e1,r,e2"
		answer = self.graph.run(sql).data()
		return answer

	#查找entity1及其对应的关系
	def find_relation_by_node_one(self,entity1):
		sql = "MATCH (n1:term)-[rel]->(n2:term) WHERE n1.name=\"" +str(entity1)+"\" RETURN n1,rel,n2"
		answer = self.graph.run(sql).data()
		return answer

	#查找entity2及其对应的关系
	def find_relation_by_node_two(self, entity2):
		sql = "MATCH (n1:term)-[rel]->(n2:term) WHERE n2.name=\"" +str(entity2)+"\" RETURN n1,rel,n2"
		answer = self.graph.run(sql).data()
		return answer

	#根据entity1和关系查找enitty2
	def find_other_node1(self,entity, relation):
		sql = "MATCH (n1:term{name:\"" + str(entity) + "\"})- [rel{relation:\""+str(relation)+"\"}]->(n2) RETURN n1, rel, n2"
		answer = self.graph.run(sql).data()
		return answer

	def find_other_node2(self, entity, relation):
		answer = self.graph.run("MATCH (n1)- [rel {relation:\""+str(relation)+"\"}] -> (n2 {name:\"" + str(entity) + "\"}) RETURN n1,rel,n2" ).data()
		return answer

	#增加一个节点
	def add_node(self, nodename, nodeclass, nodeid):
		sql = "CREATE (n:term{name:\"" + nodename + "\", nodeclass:\"" + nodeclass + "\", nodeid:\"" + nodeid + "\"})"
		return self.graph.run(sql)

	#设置节点属性
	def set_node_properties(self, nodeid, property):
		sql = "MATCH (n:term{nodeid:\"" + nodeid + "\"}) SET n.properties=\"" + property + "\""
		return self.graph.run(sql)

	#增加一个关系
	def add_relation(self, relation, id1, id2):
		sql = "MATCH (n1:term{nodeid:\"" + id1 + "\"}), (n2:term{nodeid:\"" + id2 + "\"}) CREATE (n1)-[:rel{relation:\"" + relation + "\"}]->(n2)"
		return self.graph.run(sql)
	
	#根据两个实体查询它们之间的最短路径

	def find_shotest_path(self,entity1,entity2):
		answer = self.graph.run("MATCH (p1{name:\"" + str(entity1) + "\"}),(p2{name:\"" + str(
			entity2) + "\"}),p=shortestpath((p1)-[rel*]-(p2)) RETURN rel").evaluate()

		relationDict = []
		if (answer is not None):
			for x in answer:
				tmp = {}
				start_node = x.start_node
				end_node = x.end_node
				tmp['n1'] = start_node
				tmp['n2'] = end_node
				tmp['rel'] = x
				relationDict.append(tmp)
		return relationDict

	def find_node1_node2(self, entity1, entity2):

		sql = "MATCH (n1{name:\"" + str(entity1) + "\"})- [rel] -> (n2 {name:\"" + str(entity2) + "\"}) RETURN n1,rel,n2"
		answer = self.graph.run(sql).data()

		return answer

	def find_entity_relation(self, entity1, relation,entity2):
		answer = self.graph.run("MATCH (n1{name:\"" + str(entity1) + "\"})- [rel{relation:\""+str(relation)+"\"}] -> (n2{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()

		return answer

	def parse_answer(self, answer):
		print(type(answer))
		print(len(answer))
		#for ret in answer:


neodb = KGneo4j()
neodb.connect_db()

if __name__ == '__main__':
	db = KGneo4j()
	db.connect_db()
	ret = db.find_shotest_path('钟南山', '上海医科大学')
