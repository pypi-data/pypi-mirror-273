""" Utils for S3

  


"""
import boto3
import pandas as pd
from io import StringIO
import time
import random
from datetime import datetime


from utilmy import log,loge


def test_lock():
    ### python util_s3.py test()
    #s3_csv = S3UpdatecsvwithLock('s3://bucket/csv_file.csv"')
    #s3_csv.update_csv(newrow=['Rohn', 75], retries=5, backoff_in_seconds=1)
    s3lock = S3lock('s3://bucket')
    s3lock.lock('csv_file.csv.lock')

def test_unlock():
  s3lock = S3lock('s3://bucket')
  s3lock.unlock('csv_file.csv.lock')

def test_csv_update():
  s3_csv = S3UpdatecsvwithLock('s3://bucket/csv_file.csv', 's3://bucket')
  s3_csv.update_csv(newrow=['Rohn', 75])

class S3lock:
    def __init__(self, dirlock:str, ntry_max=10, ntry_sleep=1):
        self.s3 = boto3.client('s3')
        self.dirlock = dirlock
        #self.bucket, self.lock_key = dirlock.replace("s3://", "").split('/', 1)
        self.ntry_max   = ntry_max
        self.ntry_sleep = ntry_sleep

    def to_int(self, x):
        try:
            return int(x)
        except:  
            return -1

    def sleep(self, ntry):
        print(f"Retry - {ntry}")      
        print(f"Retrying in {self.ntry_sleep * 2**ntry + random.uniform(0, 1)}")
        time.sleep( self.ntry_sleep * 2**ntry + random.uniform(0, 1) )              

    def lock(self, dirfile:str):

        dirfile= self.dirlock + "/" + str(hash(dirfile))
        bucket, lock_key = dirfile.replace("s3://", "").split('//', "/").split('/', 1)
      
        try:
            self.s3.head_object(Bucket= bucket, Key= lock_key)
        except Exception as e:
            self.s3.put_object(Bucket=bucket, Key=lock_key, Body='0')
          
        ntry = 0
        while ntry < self.ntry_max:
            lock_code = self.s3.get_object(Bucket= bucket, Key= lock_key)["Body"].read().decode()
            if self.to_int(lock_code) == 0:
                break

            ntry+=1
            self.sleep(self, ntry)


        if  ntry >= self.ntry_max:
            print("Maximum retries reached. File has been locked by someone else.")
            return False
        
        ntry = 0
        while ntry < self.ntry_max:
            lock_code1 = str(time.time_ns())
            self.s3.put_object(Bucket= bucket, Key= lock_key, Body=lock_code1)
            lock_code2 = self.s3.get_object(Bucket= bucket, Key= lock_key)["Body"].read().decode()

            if lock_code2 == lock_code1:
                print("File Locked")
                break

            ntry+=1
            self.sleep(self, ntry)


        if  ntry >= self.ntry_max:
            print("Maximum retries reached. The File is in use.")
            return False

        return True
    

    def unlock(self, dirfile:str):
        dirfile= self.dirlock + "/" + str(hash(dirfile))
        bucket, lock_key = dirfile.replace("s3://", "").split('//', "/").split('/', 1)
        ntry = 0
        while ntry < self.ntry_max:
            self.s3.put_object(Bucket= bucket, Key= lock_key, Body='0')
            lock_code = self.s3.get_object(Bucket= bucket, Key= lock_key)["Body"].read().decode()
            if self.to_int(lock_code) == 0:
                print("File Unlocked")
                break

            ntry+=1
            self.s3.put_object(Bucket= bucket, Key= lock_key, Body='0')
            self.sleep(self, ntry)
            
        if  ntry >= self.ntry_max:
            print("Maximum retries reached. Unable to unlock file after update.")
            return False
        
        return True


class S3UpdatecsvwithLock:
    def __init__(self, dir:str, dirlock:str):
        self.s3 = boto3.client('s3')
        self.bucket, self.csv_key = dir.replace("s3://", "").split('/', 1)
        self.lock_key = f"{self.csv_key}.lock"
        self.lock = S3lock(dirlock)

    def key_exists(self):
        try:
            # Check if the csv file is there in the bucket
            self.s3.head_object(Bucket=self.bucket, Key=self.csv_key)
            time.sleep(1)  # Wait if lock exists
            print("CSV file exists in the Bucket")
            return True
        except self.s3.exceptions.ClientError as e:
            print("CSV in the bucket - {}".format(e))
            return False
    
    def create_csv(self):
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            columns = ['Student', 'Score', 'Time']
            students = [['John', 88, now],]
            df = pd.DataFrame(students, columns = columns)
            csv_create = StringIO()
            df.to_csv(csv_create, index=False)
            self.s3.put_object(Bucket=self.bucket, Key=self.csv_key, Body=csv_create.getvalue())
            print("New CSV File created")
            return True
        except self.s3.exceptions.ClientError as e:
            print("Error creating CSV - {}".format(e))
            return False
    
    def write_csv(self, newrow):
        obj = self.s3.get_object(Bucket=self.bucket, Key=self.csv_key)
        df = pd.read_csv(obj['Body'])
        
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            newrow.append(now)
            new_row = pd.DataFrame([newrow], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            self.s3.put_object(Bucket=self.bucket, Key=self.csv_key, Body=csv_buffer.getvalue())
            print("CSV File Updated")
        except self.s3.exceptions.ClientError as e:
            print(f"Error updating csv file : {e}")            
            
    
    def update_csv(self, newrow):
        if self.s3 is not None:
            if not self.key_exists():
                self.create_csv()
            lock = self.lock.lock(self.lock_key)
            if lock:
                self.write_csv(newrow)
                unlock = self.lock.unlock(self.lock_key)
                if not unlock:
                    print("File could not be Unlocked")
            else:
                print("Failed to update CSV File")
            
        else:
            print("Unable to connect to S3 storage")
            return "Unable to connect to S3 storage"


if __name__ == "__main__":
    import fire 
    fire.Fire()



