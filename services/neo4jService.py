from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship

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
    

def insert_to_neo4j(df):

    graph = Graph("bolt://localhost:7687", user="neo4j", password="00000000")

    # Assuming you have a DataFrame named 'df' with your data
    # You can read the data from your CSV file using pandas like this:
    # df = pd.read_csv('your_data.csv')

    # Iterate through the DataFrame and create nodes for Organizations and Titles
    for index, row in df.iterrows():
        # Create an Organization node for each row
        organization = Node("Organization", name=row["Organizations"])

        # Create a Title node with the specified properties
        title = Node("Title", 
                     name=row["Tense"],
                     Date=row["Date"],
                     Title=row["Title"],
                     Text=row["Text"],
                     Category=row["Category"],
                     site=row["site"],
                     Tense=row["Tense"])

        # Create a relationship between Organization and Title nodes
        relation = Relationship(organization, "ABOUT", title)

        # Merge (create or update) the nodes and relationship in the Neo4j database
        graph.merge(organization, "Organization", "name")
        graph.merge(title, "Title", "Title")
        graph.merge(relation)

    print("Data inserted into Neo4j successfully.")
