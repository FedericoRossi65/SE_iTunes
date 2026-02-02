from database.DB_connect import DBConnect
from model.album import Album

class DAO:

    @staticmethod
    def get_album_nodes(durata):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print('Errore connessione database')
            return None
        cursor = cnx.cursor(dictionary=True)
        query = '''select a.id,a.title,a.artist_id,sum(t.milliseconds)/60000 as duration
                    from album a,track t
                    where a.id = t.album_id
                    group by a.id,a.title,a.artist_id
                    having sum(t.milliseconds)/60000 > %s
                                         '''
        try:
            cursor.execute(query,(durata,))
            for row in cursor:
                result.append(Album(**row))

            print(result)
        except Exception as e:
            print(f'Errore nella query: {e}')
        finally:
            cursor.close()
            cnx.close()
        return result

    def get_edges(durata):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print('Errore connessione database')
            return None
        cursor = cnx.cursor()
        query = '''select al1.id as a1,al2.id as a2
from album al1,album al2,track t1,track t2,playlist_track p1,playlist_track p2
where al1.id = t1.album_id
and t1.id = p1.track_id
and al2.id = t2.album_id
and t2.id = p2.track_id
and p1.playlist_id = p2.playlist_id
and al1.id > al2.id
and al1.id in (select a.id
                    from album a,track t
                    where t.album_id = a.id
                    group by a.id,a.title,a.artist_id
                    having sum(t.milliseconds)/60000 > %s)
and al2.id in (select a.id
                    from album a,track t
                    where t.album_id = a.id
                    group by a.id,a.title,a.artist_id
                    having sum(t.milliseconds)/60000 > %s)
GROUP by al1.id,al2.id'''
        try:
            cursor.execute(query, (durata,durata,))
            for row in cursor:
                result.append(row)

            print(result)
        except Exception as e:
            print(f'Errore nella query: {e}')
        finally:
            cursor.close()
            cnx.close()
        return result


