from neo4j import GraphDatabase

class Neo4jDB:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def insert_data(self, data):
        with self._driver.session() as session:
            session.write_transaction(self._insert_data, data)

    @staticmethod
    def _insert_data(tx, data):
        for row in data.itertuples(index=False):
            # Create a node for Title with properties and connect it to Organizations
            tx.run(
                """
                MERGE (title:Title {name: $title, Date: $date, Text: $text, Category: $category, Tense: $tense, Site: $site})
                MERGE (organization:Organization {name: $organization})
                MERGE (title)-[]->(organization)
                """,
                title=row.Title,
                date=row.Date,
                text=row.Text,
                category=row.Category,
                tense=row.Tense,
                site=row.site, 
                organization=row.Organizations,
            )

neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "00000000"

# Create an instance of the Neo4jDB class
db = Neo4jDB(neo4j_uri, neo4j_user, neo4j_password)

def test_connection():
    try:
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        with driver.session() as session:
            print("Connected to Neo4j")
            return True
    except Exception as e:
        print(f"Connection to Neo4j failed: {str(e)}")
        return False