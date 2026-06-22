import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

class DownloadHistoric(Base):
    __tablename__ = 'download_historic'
    id = Column(Integer, primary_key=True)
    suggested_file_name = Column(String)
    folder_path = Column(String)
    status = Column(String)
    download_time = Column(DateTime)

class Historic(Base):
    __tablename__ = 'historic'
    id = Column(Integer, primary_key=True)
    site = Column(String)
    name = Column(String)
    download_time = Column(DateTime)
    fav = Column(Boolean, default=False)
    folder = Column(String, default="default")

class ConsoleHistoric(Base):
    __tablename__ = 'console_historic'
    id = Column(Integer, primary_key=True)
    command = Column(String)

def init_db(db_path='sqlite:///configs/app.db'):
    # check_same_thread=False + scoped_session: cada thread recebe sua própria
    # Session (thread-local). Antes era UMA Session global compartilhada entre
    # threads — origem de travamentos/corrupção intermitentes no SQLite.
    engine = create_engine(db_path, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine))

# `session` é um scoped_session: encaminha .query/.add/.commit/... para a Session
# da thread atual, então todos os call sites existentes continuam funcionando.
session = init_db()

def register_download_historic(suggested_file_name: str, folder_path: str, status: str,
                               download_time: datetime.datetime) -> DownloadHistoric:
    download_historic = DownloadHistoric(suggested_file_name=suggested_file_name, 
                                         folder_path=folder_path, 
                                         status=status, 
                                         download_time=download_time)
    session.add(download_historic)
    session.commit()
    return download_historic

def recover_download_historic(f: str = "", limit: int = 20, order_desc=False, offset: int = 0):
    # Sempre retorna LISTA, sempre ordenada (por data), com limit/offset aplicados
    # de forma consistente (antes: lista sem ordem quando f vazio, Query quando
    # filtrado — o que ainda quebrava paginação e `if bool(...)`).
    query = session.query(DownloadHistoric)
    if f:
        query = query.filter(DownloadHistoric.folder_path.like(f'%{f}%') |
                             DownloadHistoric.suggested_file_name.like(f'%{f}%'))
    col = DownloadHistoric.download_time
    query = query.order_by(col.desc() if order_desc else col.asc())
    if offset:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def remove_download_historic_item(download_data: DownloadHistoric, remove_view: bool = False, widget=None, layout=None):
    session.query(DownloadHistoric).filter_by(id=download_data.id).delete()
    session.commit()
    if remove_view:
        layout.removeWidget(widget)
        widget.deleteLater()
        layout.update()

def update_download_status(download_id: int, status: str) -> bool:
    item = session.query(DownloadHistoric).filter_by(id=download_id).first()
    if item:
        item.status = status
        session.commit()
        return True
    return False

def update_historic(site: str, id: int, fav: bool, folder: str="default"):
    historic = session.query(Historic).filter_by(id=id, site=site).first() 
    if historic:
        historic.fav = fav
        historic.folder = folder
        session.commit()
        return True
    return False

def register_historic(site: str, name: str, download_time: datetime.datetime, fav: bool=False, folder: str="default"):
    # Idempotente: se o site já existe, atualiza a visita/título em vez de criar
    # uma nova linha (antes, cada navegação podia duplicar o histórico).
    existing = session.query(Historic).filter_by(site=site).first()
    if existing:
        existing.download_time = download_time
        if name:
            existing.name = name
        session.commit()
        return existing
    historic = Historic(site=site, name=name, fav=fav, download_time=download_time, folder=folder)
    session.add(historic)
    session.commit()
    return historic

def recover_historic(f: str = "", limit: int = 20, order_desc=False, offset: int = 0):
    query = session.query(Historic)
    if f:
        query = query.filter(Historic.site.like(f'%{f}%'))
    col = Historic.download_time
    query = query.order_by(col.desc() if order_desc else col.asc())
    if offset:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def recover_favorities(limit: int = 20, order_desc=False):
    query = session.query(Historic).filter(Historic.fav == True).order_by(
        Historic.site.desc() if order_desc else Historic.site.asc())
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def remove_historic_item(id: int, widget=None, layout=None, remove_view=True):
    session.query(Historic).filter_by(id=id).delete()
    session.commit()
    if remove_view:
        layout.removeWidget(widget)
        widget.deleteLater()
        layout.update()

def register_console_historic(command: str):
    console_historic = ConsoleHistoric(command=command)
    session.add(console_historic)
    session.commit()

def recover_console_historic(command: str, prev_next: str):
    # Guardas contra None: antes fazia .first().command direto e estourava
    # AttributeError quando não havia linha correspondente.
    if not command:
        row = session.query(ConsoleHistoric).order_by(ConsoleHistoric.id.desc()).first()
        return row.command if row else ""
    query = session.query(ConsoleHistoric)
    if prev_next == "prev":
        row = query.filter(ConsoleHistoric.command < command).order_by(ConsoleHistoric.command.desc()).first()
        return row.command if row else command
    elif prev_next == "next":
        row = query.filter(ConsoleHistoric.command > command).order_by(ConsoleHistoric.command.asc()).first()
        return row.command if row else command
    return ""

def remove_console_historic(command: str):
    session.query(ConsoleHistoric).filter_by(command=command).delete()
    session.commit()

