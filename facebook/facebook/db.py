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
    
    def save_comment(self, comment_data: dict):
        user_id = self.save_user(comment_data)
        self.save_comment_details(user_id, comment_data)
        self.connection.commit()

    def save_user(self, comment_data: dict) -> int: 
        name = comment_data["name"]
        link = comment_data["link"]
        self.cursor.execute("""
        INSERT INTO users (name, link)
        VALUES(%s, %s)
        ON CONFLICT (name, link) DO UPDATE SET name = %s
        RETURNING id;""", (name, link, name))
        return self.cursor.fetchone()[0]
    
    def save_comment_details(self, user_id, comment_data):
        comment = comment_data["comment"]
        timestamp = comment_data["timestamp"]
        self.cursor.execute("""
        INSERT INTO comments (user_id, comment, timestamp)
        VALUES (%s, %s, to_timestamp(%s))
        ON CONFLICT (user_id, comment, timestamp) DO NOTHING;
        """, (user_id, comment, timestamp))
