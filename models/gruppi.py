from database.db_connection import Database
from models.db_items import GruppoItem


class Gruppi(Database):
    def __init__(self, db_name='gruppi.db'):
        super().__init__(db_name)
        self.create_table()

    def create_table(self):
        self.execute_query('''
        CREATE TABLE IF NOT EXISTS Gruppi (
            id INTEGER PRIMARY KEY,
            id_progetto INTEGER,
            nome TEXT NOT NULL,
            link TEXT,
            paese TEXT,
            regione TEXT,
            provincia TEXT,
            citta TEXT,
            FOREIGN KEY(id_progetto) REFERENCES Progetto(id)
        )
        ''')
        self.conn.commit()

    def add_gruppo(self, id_progetto, nome, link, paese, regione, provincia, città):
        self.execute_query('INSERT INTO Gruppi (id_progetto, nome, link, paese, regione, provincia, città) VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (id_progetto, nome, link, paese, regione, provincia, città))
        self.conn.commit()

    def get_gruppo(self, id_gruppo):
        return self.execute_query('SELECT * FROM Gruppi WHERE id = ?', (id_gruppo,)).fetchone()

    def update_gruppo(self, id_gruppo, **kwargs):
        updates = ', '.join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values())
        values.append(id_gruppo)
        self.execute_query(f'UPDATE Gruppi SET {updates} WHERE id = ?', values)
        self.conn.commit()

    def delete_gruppo(self, id_gruppo):
        self.execute_query('DELETE FROM Gruppi WHERE id = ?', (id_gruppo,))
        self.conn.commit()

if __name__ == '__main__':
    Gruppi()
