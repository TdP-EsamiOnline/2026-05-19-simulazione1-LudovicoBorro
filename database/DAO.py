from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre

class DAO:

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """
            select *
            from genre
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtistsByGenre(genre_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """
                select distinct(a.ArtistId), a.Name
                from artist a, album al, track t 
                where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.GenreId = %s
        """

        cursor.execute(query, (genre_id,))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCustomerByArtistAndGenre(artist_id, genre_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """
                select distinct(i2.CustomerId)
                from track t, invoiceline i, album a, invoice i2 
                where t.TrackId = i.TrackId and a.AlbumId  = t.AlbumId and i.InvoiceId = i2.InvoiceId 
                and t.GenreId = %s and a.ArtistId = %s
                """

        cursor.execute(query, (genre_id, artist_id))

        for row in cursor:
            result.append(row["CustomerId"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistiWPopularity():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """
                select a.ArtistId, count(distinct t.TrackId) as Popularity
                from album a, track t, invoiceline i 
                where a.AlbumId = t.AlbumId and t.TrackId = i.TrackId 
                group by a.ArtistId 
                """

        cursor.execute(query)

        for row in cursor:
            result.append((row["ArtistId"], row["Popularity"]))

        cursor.close()
        conn.close()
        return result