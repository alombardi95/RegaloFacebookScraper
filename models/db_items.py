from app import db


class GruppoItem(db.Model):
    __tablename__ = 'gruppi'

    link = db.Column(db.String(200), primary_key=True)
    nome = db.Column(db.String(100))
    paese = db.Column(db.String(100))
    regione = db.Column(db.String(100))
    provincia = db.Column(db.String(100))
    citta = db.Column(db.String(100))
    data_creazione = db.Column(db.DateTime)
    dettagli = db.relationship('DettagliGruppoItem', backref='gruppi')

    def __repr__(self):
        return f"<GruppoItem(id={self.link}, nome={self.nome})>"


class DettagliGruppoItem(db.Model):
    __tablename__ = 'dettagli_gruppo'

    id = db.Column(db.Integer, primary_key=True)
    id_gruppo = db.Column(db.String(200), db.ForeignKey('gruppi.link'))
    timestamp = db.Column(db.DateTime)
    numero_membri = db.Column(db.Integer)
    numero_admin = db.Column(db.Integer)
    posts_mensili = db.Column(db.Integer)
    posts_giornalieri = db.Column(db.Integer)
    ultima_modifica = db.Column(db.DateTime)

    def __repr__(self):
        return f"<DettagliGruppoItem(id={self.id}, id_gruppo={self.id_gruppo})>"
