from pymongo import MongoClient
from pymongo.cursor import CursorType
import datetime

'''
데이터베이스 이름 : pengsoo
테이블 : User(name, pwd)
테이블 : Command(input, output, device, date)
ex) {"hi", "Hi, How are you?", "speaker", new Date()} 
'''

class MongoDB:

    def __init__(self):    
        self.host = "127.0.0.1"
        self.port = "27017"

        self.mongo = MongoClient(self.host, int(self.port))
        print(self.mongo)
        #print(self.mongo.database_names())
        
        self.database = self.mongo['pengsoo']
        self.collection = self.database['command']    
        self.now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')        


    # Command 테이블에 데이터 추가
    def insert_command_one(self, command, output, device):
        data = {'input':command,
                'output': output,
                'device': device,
                'date': self.now }

        result = self.collection.insert_one(data).inserted_id
        print('MongoDB-Insert : ', result)
        return result

    def insert_command_many(self, data, db_name=None, collection_name=None):
        result = self.collection[db_name][collection_name].insert_many(data).inserted_id
        return result

    # Command 테이블에 데이터 수정
    def update_command_one(self, data):
        tmp_data = {'input':data.command, 'output': data.output, 'device': data.device}

        result = self.collection.update_one(tmp_data).upserted_id
        print('MongoDB-Update : ', result)
        return result

    # Command 테이블에 데이터 삭제
    def delete_command(self, condition=None, db_name=None, collection_name=None):
        result = self.collection[db_name][collection_name].delete_one(condition)
        return result

    # Command 테이블에 데이터 불러오기
    def select_command_One(self):
        return self.collection.find_one()

    def select_command_All(self):
        return self.collection.find()


'''
#[사용예제]
if __name__ == "__main__":
    db = MongoDB()        
    # 데이터 삽입
    ret = db.insert_command_one('stop', 'yes,sir!', 'speaker')
    print(ret)
    # 데이터 수정
    #ret = db.update_command_one({'input':'love you', 'output':'what?'})
    # 방금 삽입된 데이터 호출
    ret2 = db.select_command_One()
    print(ret2)
'''    