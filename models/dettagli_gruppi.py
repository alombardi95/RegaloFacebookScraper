from database.db_connection import Database
from models.db_items import DettagliGruppoItem


class DettagliGruppi(Database):
    def __init__(self, db_name='gruppi.db'):
        super().__init__(db_name)
        self.create_table()

    def create_table(self):
        self.execute_query('''
        CREATE TABLE IF NOT EXISTS Dettagli_Gruppi (
            id INTEGER PRIMARY KEY,
            id_gruppo INTEGER,
            data_aggiornamento DATE,
            numero_membri INTEGER,
            numero_admin INTEGER,
            nuovi_posts INTEGER,
            data_creazione DATE,
            FOREIGN KEY(id_gruppo) REFERENCES Gruppi(id)
        )
        ''')
        self.conn.commit()

    def add_dettaglio(self, dettaglio: DettagliGruppoItem):
        self.add_dettaglio(
            dettaglio.id_gruppo,
            dettaglio.data_aggiornamento,
            dettaglio.numero_membri,
            dettaglio.numero_admin,
            dettaglio.nuovi_posts
        )

    def add_dettaglio(self, id_gruppo, data_aggiornamento, numero_membri, numero_admin, nuovi_posts):
        self.execute_query('INSERT INTO Dettagli_Gruppi (id_gruppo, data_aggiornamento, numero_membri, numero_admin, nuovi_posts) VALUES (?, ?, ?, ?, ?)',
                           (id_gruppo, data_aggiornamento, numero_membri, numero_admin, nuovi_posts))
        self.conn.commit()

    def get_dettaglio(self, id_dettaglio) -> DettagliGruppoItem:
        result = self.execute_query('SELECT * FROM Dettagli_Gruppi WHERE id = ?', (id_dettaglio,)).fetchone()
        return DettagliGruppoItem(**result)

    def update_dettaglio(self, id_dettaglio, **kwargs):
        updates = ', '.join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values())
        values.append(id_dettaglio)
        self.execute_query(f'UPDATE Dettagli_Gruppi SET {updates} WHERE id = ?', values)
        self.conn.commit()

    def delete_dettaglio(self, id_dettaglio):
        self.execute_query('DELETE FROM Dettagli_Gruppi WHERE id = ?', (id_dettaglio,))
        self.conn.commit()
