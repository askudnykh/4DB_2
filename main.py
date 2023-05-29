from module import Publisher, Book, Shop, Stock, Sale, create_tables
import sqlalchemy
from sqlalchemy.orm import sessionmaker

DSN = "postgresql://postgres:postgres@localhost:5432/SQL4_hw"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='Пушкин')
publisher2 = Publisher(name='Лермонтов')

book1 = Book(title='Онегин', publisher=publisher1)
book2 = Book(title='Капитанская дочка', publisher=publisher1)
book3 = Book(title='Кавказский пленник', publisher=publisher2)

shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')

stock1 = Stock(book=book1, shop=shop1, count=2)
stock2 = Stock(book=book2, shop=shop1, count=3)
stock3 = Stock(book=book3, shop=shop1, count=4)
stock4 = Stock(book=book1, shop=shop2, count=5)
stock5 = Stock(book=book1, shop=shop3, count=6)

sale1 = Sale(price=100, date_sale='01.11.2020', stock=stock1, count=1)
sale2 = Sale(price=200, date_sale='02.11.2020', stock=stock2, count=2)
sale3 = Sale(price=350, date_sale='03.11.2020', stock=stock3, count=1)
sale4 = Sale(price=400, date_sale='04.11.2020', stock=stock5, count=1)

session.add_all(
    [publisher1, publisher2, book1, book2, book3, shop1, shop2, shop3, stock1, stock2, stock3, stock4, stock5, sale1,
     sale2, sale3, sale4])
session.commit()
inp_publisher = input('Автор')
subq = session.query(Publisher).filter(Publisher.name == inp_publisher).subquery()

result = session.query(Sale.price, Sale.count, Sale.date_sale, Book.title, Shop.name).join(Stock,
                                                                                           Sale.id_stock == Stock.id).join(
    Shop, Stock.id_shop == Shop.id).join(Book, Book.id == Stock.id_book).join(subq, Book.id_publisher == subq.c.id)

for sale_, book_, shop_ in result:
    print(f'{book_.title} | {shop_.name} | {sale_.price * sale_.count} | {sale_.date_sale}')

session.close()
