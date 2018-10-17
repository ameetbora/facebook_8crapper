import psycopg2

conn_str = "dbname='facebook_comments' user='postgres'" # Might want to change this

def truncate(value: str, length: int) -> str:
    if len(value) > length:
        return value[:length] + "..."
    
    return value


class db:
    def __init__(self):
        self.connection = psycopg2.connect(conn_str)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()
    
    def rollback(self):
        self.connection.rollback()
    
    def get_highest_cn(self) -> int:
        self.cursor.execute("""SELECT highest FROM comment_number ORDER BY highest DESC LIMIT 1""")
        return self.cursor.fetchone()[0]
    
    def update_highest_cn(self, new_highest: int):
        self.cursor.execute("""INSERT INTO comment_number (highest) VALUES ({});""".format(new_highest))
        self.commit()
    
    def save_comment(self, comment_data: dict, supplier_id: int):
        user_id = self.save_user(comment_data)
        self.save_comment_details(user_id, supplier_id, comment_data)
        self.commit()

    def save_like(self, user_data: dict, supplier_id: int):
        user_id = self.save_user(user_data)
        self.save_like_details(user_id, supplier_id)
        self.commit()

    def save_user(self, comment_data: dict) -> int: 
        name = truncate(comment_data["name"], 150)
        link = truncate(comment_data["link"], 900)
        self.cursor.execute("""
        INSERT INTO users (name, link)
        VALUES('Jen Duff', 'https://www.facebook.com/jen.duff.52?ref=br_rs')
        ON CONFLICT (name, link) DO UPDATE SET name = 'Jen Duff'
        RETURNING id;""", (name, link, name))
        return self.cursor.fetchone()[0]
    


    def save_comment_details(self, user_id: int, supplier_id: int, comment_data: dict):
        comment = truncate(comment_data["comment"], 5000)

        # Probably non need to store the entirety of very long comments in the database


        timestamp = comment_data["timestamp"]
        tagged = comment_data["tagged"]
        self.cursor.execute("""
        INSERT INTO comments (user_id, supplier_id, comment, timestamp, tagged)
        VALUES (%s, %s, %s, to_timestamp(%s), %s)
        ON CONFLICT (user_id, comment, timestamp) DO NOTHING;
        """, (user_id, supplier_id, comment, timestamp, tagged))

    def save_like_details(self, user_id: int, supplier_id: int):
        self.cursor.execute("""
        INSERT INTO likes (user_id, supplier_id)
        VALUES (%s, %s)
        ON CONFLICT (user_id, supplier_id) DO NOTHING;
        """, (user_id, supplier_id))
    
    def save_supplier(self, supplier_name, page_id) -> int:
        self.cursor.execute("""
        INSERT INTO suppliers (name, page_id)
        VALUES(%s, %s)
        ON CONFLICT (name, page_id) DO UPDATE SET name = %s
        RETURNING id;""", (supplier_name, page_id, supplier_name))
        self.commit()
        return self.cursor.fetchone()[0]

    def get_suppliers(self) -> dict:
        self.cursor.execute("""SELECT id, name, page_id FROM suppliers""")
        return self.cursor.fetchall()