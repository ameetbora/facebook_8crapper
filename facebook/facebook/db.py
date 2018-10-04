import psycopg2

conn_str = "dbname='facebook_comments' user='postgres'" # Might want to change this

class db:
    def __init__(self):
        self.connection = psycopg2.connect(conn_str)
        self.cursor = self.connection.cursor()
    
    def get_highest_cn(self) -> int:
        self.cursor.execute("""SELECT highest FROM comment_number ORDER BY highest DESC LIMIT 1""")
        return self.cursor.fetchone()[0]
    
    def update_highest_cn(self, new_highest: int):
        self.cursor.execute("""INSERT INTO comment_number (highest) VALUES ({});""".format(new_highest))
        self.connection.commit()
