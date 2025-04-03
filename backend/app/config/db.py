from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymsql://root@localhost:3306/DB NAME")
meta = MetaData()
connection = engine.connect( )