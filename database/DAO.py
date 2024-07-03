from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    @staticmethod
    def getAlbums(d):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds) as totD
                    from album a, track t
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId 
                    having totD > %s"""

        cursor.execute(query, (d,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):  # mi restituisce una lista di tuple in cui ogni elemento della
        # lista è una coppia di nodi, in quella coppia di nodi io devo mettere l'arco
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinctrow t1.AlbumId as a1, t2.AlbumId as a2
                    from track t1, track t2, playlisttrack p1, playlisttrack p2 
                    where p1.PlaylistId = p2.PlaylistId   
                    and t1.trackId = p1.trackId
                    and t2.TrackId = p2.TrackId 
                    and t1.AlbumId < t2.AlbumId"""

        cursor.execute(query)

        # distinctrow mi restituisce righe distinte, distinct prende solo l'argomento

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                # in questo modo verifico che il primo nodo dell'arco sia già stato aggiunto al grafo,
                # perché l'idMap l'ho fatta a partire dai nodi del grafo
                result.append((idMap[row["a1"]], idMap[row["a2"]]))
                # l'append lo faccio solo se i nodi già esistono, cosìsono sicura di filtrare album che durano più di d

        cursor.close()
        conn.close()
        return result
