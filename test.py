import unittest
import time
class TestConnections(unittest.TestCase):

    def setUp(self):
        print("Waiting for mySQL to finish booting")
        time.sleep(15)
        import mysql.connector as mysql
        self.db = mysql.connect(
           host = "127.0.0.1",
           database = "reportdb",
           user = "user",
           passwd = "password"
        )
        
        
    def test_connectdb(self):
        print("Running ConnectDB test")
        print(self.db)

    def test_readdata(self):
        print("Running Read Data")
        print("Checking reports table")
        cursor = self.db.cursor()
        cursor.execute("select * from reports")
        records = cursor.fetchall()
        assert cursor.rowcount>=1,"There should be one or more reports records"
        cursor.execute("select * from ingests")
        records = cursor.fetchall()
        assert cursor.rowcount>=1,"There should be one or more ingests records"
        cursor.close()

    def test_writedata(self):
        print("Running Write Data")
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO reports (filename,created_at,ingested_at,currentloc) VALUES (%s, %s, %s, %s)",("abc.pdf","2020-01-06 15:55:55","2020-01-06 16:33:33","/mnt/raw/reports/"))
        self.db.commit()
        assert cursor.rowcount>=1,"There should be one report inserted"
        cursor.execute("INSERT INTO ingests (text,section,created_at,ingest_id,predicted_category,annotated_category) VALUES (%s, %s, %s, %s,%s,%s)",("This is the weather for singapore","observation","2020-01-06 15:55:55","1","DOCTRINE","DOCTRINE")) 
        cursor.close()

if __name__ == '__main__':
    unittest.main()
