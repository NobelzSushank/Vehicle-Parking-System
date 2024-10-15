import mysql.connector;
import json
from datetime import datetime

class DBOperation():
    def __init__(self):
        file = open("./config.json")
        datadic = json.loads(file.read())
        file.close()
        self.myDb = mysql.connector.connect(
            host = "localhost",
            user = datadic['username'],
            passwd = datadic['password'],
            database = datadic['database']
        )

    def createTables(self):
        cursor = self.myDb.cursor()
        cursor.execute("DROP TABLE if exists admins")
        cursor.execute("DROP TABLE if exists slots")
        cursor.execute("DROP TABLE if exists vehicles")
        cursor.execute("CREATE TABLE admins ( id int(255) AUTO_INCREMENT PRIMARY KEY, username varchar(30), password varchar(30), created_at varchar(30), updated_at varchar(30))")
        cursor.execute("CREATE TABLE slots ( id int(255) AUTO_INCREMENT PRIMARY KEY, vehicle_id varchar(30), space_for int(25), is_empty int(25), created_at varchar(30), updated_at varchar(30))")
        cursor.execute("CREATE TABLE vehicles ( id int(255) AUTO_INCREMENT PRIMARY KEY, name varchar(30), mobile varchar(30), entry_time varchar(30), exit_time varchar(30), is_exist varchar(30), vehicle_no varchar(30), vehicle_type varchar(30), created_at varchar(30), updated_at varchar(30))")
        cursor.close()

    def insertOneTimeData(self, space_for_two, space_for_four):
        print("insert slots")
        print(space_for_two)
        cursor = self.myDb.cursor()
        for x in range(space_for_two):
            cursor.execute("INSERT into slots (space_for, is_empty) VALUES ('2', '1')")
            self.myDb.commit()
        
        for x in range(space_for_four):
            cursor.execute("INSERT INTO slots (space_for, is_empty) VALUES ('4', '1')")
            self.myDb.commit()

        cursor.close()

    def insertAdmin(self, username, password):
        print("insert admin")
        cursor = self.myDb.cursor()
        val = (username, password)
        cursor.execute("INSERT INTO admins (username, password) VALUES (%s,%s)", val)

        self.myDb.commit()
        cursor.close()

    def doAdminLogin(self, username, password):
        cursor = self.myDb.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = '"+username+"' AND password='"+password+"'")
        data = cursor.fetchall()
        cursor.close()
        if len(data) > 0:
            return True
        else: 
            return False

    def getSlotSpace(self):
        cursor = self.myDb.cursor()
        cursor.execute("SELECT * FROM slots")
        data = cursor.fetchall()
        cursor.close()
        return data

    def getCurrentVehicle(self):
        cursor = self.myDb.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE is_exist='0'")
        data = cursor.fetchall()
        cursor.close()
        return data

    def getAllVehicle(self):
        cursor = self.myDb.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE is_exist='1'")
        data = cursor.fetchall()
        cursor.close()
        return data

    def addVehicles(self, name, vehicleNo, mobile, vehicle_type):
        spaceId = self.spaceAvailable(vehicle_type)
        if spaceId:
            currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = (name, mobile, str(currentDate), '',  '0', vehicleNo, str(currentDate), str(currentDate), vehicle_type)
            cursor = self.myDb.cursor()
            try:
                cursor.execute("INSERT INTO vehicles (name, mobile, entry_time, exit_time, is_exist, vehicle_no, created_at, updated_at, vehicle_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
                self.myDb.commit()
                lastId = cursor.lastrowid
                cursor.execute("UPDATE slots SET vehicle_id='"+str(lastId)+"', is_empty='0' WHERE id='"+str(spaceId)+"'")
                self.myDb.commit()
                cursor.close()
                return True
            except:
                cursor.close()
                return False
        else:
            return "No Space Available for Parking"

    def spaceAvailable(self, vehicleType):
        cursor = self.myDb.cursor()
        cursor.execute("SELECT * FROM slots WHERE is_empty='1' AND space_for='"+str(vehicleType)+"'")
        data = cursor.fetchall()
        cursor.close()

        if len(data) > 0:
            return data[0][0]
        else:
            return False

    def exitVehicle(self, id):
        cursor = self.myDb.cursor()
        currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE slots SET is_empty = '1', vehicle_id = '"+id+"'")
        self.myDb.commit()
        cursor.execute("UPDATE vehicles SET is_exist = '1', exit_time='"+currentDate+"' WHERE id = '"+id+"'")
        self.myDb.commit()



