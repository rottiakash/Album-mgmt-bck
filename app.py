#Interface for SQLITE
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps,dump
from flask_cors import CORS
import datetime
e = create_engine('sqlite:///app.db')
app = Flask(__name__)
api = Api(app)
CORS(app)
result = []
class getSongSearch(Resource):
    def get(self,name):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select sid,alname,genre,music_producer,mname from songs,albums where songs.alid = albums.alid and mname like '%"+name+"%';")
        for i in query.cursor.fetchall():
            dict = {'sid':i[0],
                    'albumName':i[1],
                    'genre':i[2],
                    'musicProducer':i[3],
                    'name':i[4],
                    }
            result.append(dict)
        return result

class getArtistSearch(Resource):
    def get(self,name):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select * from Artist where name like '%"+name+"%';")
        for i in query.cursor.fetchall():
            dict = {'aid':i[0],
                    'name':i[1],
                    'country':i[2],
                    'numberCopies':i[3],
                    }
            result.append(dict)
        return result

class getAlbumSearch(Resource):
    def get(self,name):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select alid,name,alname,record_label,no_of_streams from Albums,Artist where alname like '%"+name+"%' and Albums.aid=artist.aid;")
        for i in query.cursor.fetchall():
            dict = {'alid':i[0],
                    'artistName':i[1],
                    'name':i[2],
                    'recordLabel':i[3],
                    'noOfStreams':i[4]
                    }
            result.append(dict)
        return result

class getAlbumArtist(Resource):
    def get(self,aid):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select alid,name,alname,record_label,no_of_streams from Albums,Artist where albums.aid="+str(aid)+" and Albums.aid=artist.aid;")
        for i in query.cursor.fetchall():
            dict = {'alid':i[0],
                    'artistName':i[1],
                    'name':i[2],
                    'recordLabel':i[3],
                    'noOfStreams':i[4]
                    }
            result.append(dict)
        return result

class getSongAlbum(Resource):
    def get(self,alid):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select sid,alname,genre,music_producer,mname from songs,albums where songs.alid = albums.alid and songs.alid="+str(alid)+";")
        for i in query.cursor.fetchall():
            dict = {'sid':i[0],
                    'albumName':i[1],
                    'genre':i[2],
                    'musicProducer':i[3],
                    'name':i[4],
                    }
            result.append(dict)
        return result

class getAlbum(Resource):
    def get(self):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select alid,name,alname,record_label,no_of_streams from Albums,Artist where Albums.aid=artist.aid;")
        for i in query.cursor.fetchall():
            dict = {'alid':i[0],
                    'artistName':i[1],
                    'name':i[2],
                    'recordLabel':i[3],
                    'noOfStreams':i[4]
                    }
            result.append(dict)
        return result

class getSong(Resource):
    def get(self):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select sid,alname,genre,music_producer,mname from songs,albums where songs.alid = albums.alid;")
        for i in query.cursor.fetchall():
            dict = {'sid':i[0],
                    'albumName':i[1],
                    'genre':i[2],
                    'musicProducer':i[3],
                    'name':i[4],
                    }
            result.append(dict)
        return result

class getArtist(Resource):
    def get(self):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select * from Artist;")
        for i in query.cursor.fetchall():
            dict = {'aid':i[0],
                    'name':i[1],
                    'country':i[2],
                    'numberCopies':i[3],
                    }
            result.append(dict)
        return result

class insertArtist(Resource):
    def get(self,name,country,nocopies):
        result.clear()
        #Connect to databse
        conn = e.connect()
        query = conn.execute("select artist from counters")
        count = query.cursor.fetchall()[0][0]
        #Perform query and return JSON data
        values = "(%s,'%s',%s,'%s')" %(count,name,nocopies,country)
        query = conn.execute("insert into artist values"+values)
api.add_resource(getSongSearch,'/getsongsearch/<string:name>')
api.add_resource(getArtistSearch,'/getartistsearch/<string:name>')
api.add_resource(getAlbumSearch,'/getalbumsearch/<string:name>')
api.add_resource(getAlbumArtist,'/getalbumArtist/<int:aid>')
api.add_resource(getSongAlbum,'/getsongAlbum/<int:alid>')
api.add_resource(getAlbum,'/getAlbums')
api.add_resource(getSong,'/getSongs')
api.add_resource(getArtist,'/getArtists')
api.add_resource(insertArtist,'/insertArtist/<string:name>/<string:country>/<string:nocopies>')
if __name__ == '__main__':
    app.run()