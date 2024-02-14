# importing sqlite3 module
import sqlite3
 
connection = sqlite3.connect('movie_titles.db')
 
connection.execute(''' CREATE TABLE movies
         (TITLE            TEXT    NOT NULL,
         PRODUCER          TEXT    NOT NULL,
         CONTENT_RATING    TEXT    NOT NULL,
         RUNTIME_MIN       INT     NOT NULL,
         RELEASE_YEAR      INT     NOT NULL,
         GROSS_WW_INCOME   INT     NOT NULL);
         ''')
 
connection.execute("INSERT INTO movies VALUES ('The Shawshank Redemption','Frank Darabont','R',142,1994,28884716)")
connection.execute("INSERT INTO movies VALUES ('The Godfather','Francis Ford Coppola','R',202,1974,47961919)")
connection.execute("INSERT INTO movies VALUES ('The Dark Knight','Christopher Nolan','PG-13',152,2008,1029266147)")
connection.execute("INSERT INTO movies VALUES ('Schindlers List','Steven Spielberg','R',195,1993,322161245)")
connection.execute("INSERT INTO movies VALUES ('The Lord of the Rings: The Return of the King','Peter Jackson','PG-13',201,2003,1156194180)")
connection.execute("INSERT INTO movies VALUES ('The Lord of the Rings: The Fellowship of the Ring','Peter Jackson','PG-13',178,2001,883407846)")
connection.execute("INSERT INTO movies VALUES ('The Good, the Bad and the Ugly','Sergio Leone','Approved',178,1966,25100000)")
connection.execute("INSERT INTO movies VALUES ('Forrest Gump','Robert Zemeckis','PG-13',142,1994,678226465)")
connection.execute("INSERT INTO movies VALUES ('Fight Club','David Fincher','R',139,1999,101209702)")
 
connection.commit()
 
print("All movie db info")
 
cursor = connection.execute("SELECT * from movies ")
 
for row in cursor:
    print(row)

# MINIMAL CODE FOR QUERY 
#import sqlite3
#connection = sqlite3.connect('movie_titles.db')
#cursor = connection.execute("SELECT * from movies ")
#for row in cursor:
#    print(row)
