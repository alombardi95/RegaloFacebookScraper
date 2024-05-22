from database.db_connection import Database
from models.db_items import ProgettoItem


class Progetto(Database):
    def __init__(self, db_name='gruppi.db'):
        super().__init__(db_name)
        self.create_table()

    def create_table(self):
        self.execute_query('''
        CREATE TABLE IF NOT EXISTS Progetto (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def add_progetto(self, nome):
        self.execute_query('INSERT INTO Progetto (nome) VALUES (?)', (nome,))
        self.conn.commit()

    def get_progetto(self, id_progetto) -> ProgettoItem:
        result = self.execute_query('SELECT * FROM Progetto WHERE id = ?', (id_progetto,)).fetchone()
        return ProgettoItem(**result)

    def get_progetti(self) -> list[ProgettoItem]:
        results = self.execute_query('SELECT * FROM Progetto').fetchall()
        progetti = [ProgettoItem(**dict(result)) for result in results]
        return progetti

    def update_progetto(self, id_progetto: int, nome: str):
        self.execute_query('UPDATE Progetto SET nome = ? WHERE id = ?', (nome, id_progetto))
        self.conn.commit()

    def delete_progetto(self, id_progetto: int):
        self.execute_query('DELETE FROM Progetto WHERE id = ?', (id_progetto,))
        self.conn.commit()
