from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import mapped_column, sessionmaker



class ScrapypracticamlPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value 

        cuote_list = ['cuote_cant']
        for cuote in cuote_list:
            value = adapter.get(cuote)
            if value is not None:
                value = value.replace(" ", "").split("x")[0]
            adapter[cuote] = value

        prices = ['cuote_price','price']
        for p in prices:
            value = adapter.get(p)
            if value is not None:
                value = int(value.replace(".", ""))
            adapter[p] = value

        stocks = ['stock']
        for stock in stocks:
            value = adapter.get(stock)
            if value is not None:
                value = int(value.replace("(","").replace(")",""))
            adapter[stock] = value


        print(adapter)
        return item

Base = declarative_base()

class Product(Base):
    __tablename__ = 'placadevideos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    title = Column(String)
    price = Column(Integer)
    cuote_cant = Column(Integer)
    cuote_price = Column(Integer)
    stock = Column(Integer)
    calification = Column(Float)
    description = Column(String)
    time = Column(DateTime)
    #chunks = mapped_column(Vector())
    #embedding = mapped_column(Vector(3))

class PostgresqlPipeline:
    def __init__(self, db_uri):
        self.db_uri = db_uri

    # La función from_crawler se utiliza para crear una instancia de la pipeline personalizada y configurarla utilizando información proporcionada por el objeto crawler. El objeto crawler es una instancia de la clase Crawler de Scrapy y contiene información sobre la araña y la configuración de la araña en ejecución.
    @classmethod
    def from_crawler(cls, crawler):
        db_uri = crawler.settings.get('POSTGRESQL_DATABASE_URI')
        if db_uri is None:
            raise ValueError("No existe el el string de coneccion")
        return cls(db_uri)

    def open_spider(self, spider):
        self.engine = create_engine(self.db_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def close_spider(self, spider):
        self.engine.dispose()

    def process_item(self, item, spider):
        session = self.Session()
        session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        print("\nSE EJECUTO SESSION\n")
        product = Product(
            url=item['url'],
            title = item['title'],
            cuote_cant = item['cuote_cant'],
            price = item['price'],
            cuote_price = item['cuote_price'],
            stock = item['stock'],
            num_reviews = item['num_reviews'],
            calification = item['calification'],
            description=item['description'],
            time=item['time'],
            embedding = [1,2,3],
            chunks = item['chunks']
        )
        
        try:
            session.add(product)
            session.commit()
        except Exception as e:
            session.rollback()
            raise DropItem(f"Error al insertar el elemento en la base de datos: {e}")
        finally:
            session.close()

        return item