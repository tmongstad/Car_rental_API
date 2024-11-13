from neo4j import GraphDatabase
from 

# DATABASE URI and login-details
NEO4J_URI='neo4j+s://077d22f6.databases.neo4j.io'
NEO4J_USER='neo4j'
NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')

# Initiate driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

#Function that runs queries
def run_query(query, params = None):
    with driver.session() as session:
        result = session.run(query, params)
        return result.data()