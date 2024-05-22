from datetime import datetime
from dataclasses import dataclass


@dataclass
class ProgettoItem:
    id: int
    nome: str


@dataclass
class GruppoItem:
    id: int
    id_progetto: int
    nome: str
    link: str
    paese: str
    regione: str
    provincia: str
    citta: str


@dataclass
class DettagliGruppoItem:
    id: int
    id_gruppo: int
    data_aggiornamento: datetime
    numero_membri: int
    numero_admin: int
    nuovi_posts: int
