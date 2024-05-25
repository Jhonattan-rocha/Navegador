import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

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

def recover_download_historic(f: str = "", limit: int=20, order_desc=False):
    if f:
        return session.query(DownloadHistoric).filter(DownloadHistoric.folder_path.like(f'%{f}%') | 
                                                      DownloadHistoric.suggested_file_name.like(f'%{f}%')).order_by(DownloadHistoric.folder_path.desc() if order_desc else DownloadHistoric.folder_path.asc()).limit(limit)
    return session.query(DownloadHistoric).all()

def remove_download_historic_item(download_data: DownloadHistoric, remove_view: bool = False, widget=None, layout=None):
    session.query(DownloadHistoric).filter_by(id=download_data.id).delete()
    session.commit()
    if remove_view:
        layout.removeWidget(widget)
        widget.deleteLater()
        layout.update()

def update_historic(site: str, id: int, fav: bool, folder: str="default"):
    historic = session.query(Historic).filter_by(id=id, site=site).first() 
    if historic:
        historic.fav = fav
        historic.folder = folder
        session.commit()
        return True
    return False

def register_historic(site: str, name: str, download_time: datetime.datetime, fav: bool=False, folder: str="default"):
    historic = Historic(site=site, name=name, fav=fav, download_time=download_time, folder=folder)
    session.add(historic)
    session.commit()

def recover_historic(f: str = "", limit: int=20, order_desc=False):
    if f:
        return session.query(Historic).filter(Historic.site.like(f'%{f}%')).order_by(Historic.site.desc() if order_desc else Historic.site.asc()).limit(limit)
    return session.query(Historic).all()

def recover_favorities(limit: int=20, order_desc=False):
    return session.query(Historic).filter(Historic.fav == True).order_by(Historic.site.desc() if order_desc else Historic.site.asc()).limit(limit)

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
    if not command:
        return session.query(ConsoleHistoric).order_by(ConsoleHistoric.id.desc()).first().command
    query = session.query(ConsoleHistoric)
    if prev_next == "prev":
        return query.filter(ConsoleHistoric.command < command).order_by(ConsoleHistoric.command.desc()).first().command
    elif prev_next == "next":
        return query.filter(ConsoleHistoric.command > command).order_by(ConsoleHistoric.command.asc()).first().command
    return ""

def remove_console_historic(command: str):
    session.query(ConsoleHistoric).filter_by(command=command).delete()
    session.commit()

