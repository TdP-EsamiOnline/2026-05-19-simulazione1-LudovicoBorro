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
                select distinct a.ArtistId, a.Name
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
    def getArtistiWPopularityByGenre(genre_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """
                select a.ArtistId, sum(i.Quantity) as Popularity
                from album a, track t, invoiceline i 
                where a.AlbumId = t.AlbumId and t.TrackId = i.TrackId and t.GenreId = %s
                group by a.ArtistId 
                """

        cursor.execute(query, (genre_id,))

        for row in cursor:
            result.append((row["ArtistId"], row["Popularity"]))

        cursor.close()
        conn.close()
        return result

    # @staticmethod
    # def getAllArtists():
    #     conn = DBConnect.get_connection()
    #     cursor = conn.cursor(dictionary=True)
    #
    #     result = []
    #
    #     query = """
    #             select *
    #             from artist
    #             """
    #
    #     cursor.execute(query)
    #
    #     for row in cursor:
    #         result.append(Artist(**row))
    #
    #     cursor.close()
    #     conn.close()
    #     return result
    #
    # @staticmethod
    # def getAllEdges(genre_id, idMapArtist):
    #     conn = DBConnect.get_connection()
    #     cursor = conn.cursor(dictionary=True)
    #
    #     result = []
    #
    #     query = """
    #             SELECT DISTINCT al1.ArtistId AS id1, al2.ArtistId AS id2
    #             FROM album al1, track t1, invoiceline il1, invoice i1,
    #                  album al2, track t2, invoiceline il2, invoice i2
    #             WHERE al1.AlbumId = t1.AlbumId AND t1.TrackId = il1.TrackId AND il1.InvoiceId = i1.InvoiceId
    #               AND al2.AlbumId = t2.AlbumId AND t2.TrackId = il2.TrackId AND il2.InvoiceId = i2.InvoiceId
    #               AND i1.CustomerId = i2.CustomerId
    #               AND t1.GenreId = %s AND t2.GenreId = %s
    #               AND al1.ArtistId <> al2.ArtistId
    #             """
    #
    #     cursor.execute(query, (genre_id, genre_id))
    #
    #     for row in cursor:
    #         result.append((idMapArtist.get(row["id1"]), idMapArtist.get(row["id2"])))
    #
    #     cursor.close()
    #     conn.close()
    #     return result