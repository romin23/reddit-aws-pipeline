from utils.constants import ACCESS_KEY_ID, ACCESS_SECRET_KEY
import s3fs


def connect_to_s3():
    try:
        s3 =    s3fs.S3FileSystem(anon=False,
                                  key = ACCESS_KEY_ID,
                                  secret = ACCESS_SECRET_KEY)
        return s3
    except Exception as e:
        print(e)


def upload_to_s3(s3: s3fs.S3FileSystem, file_path:str, bucket:str, file_name:str):
    try:
        s3.put(file_path, bucket+'/raw/'+file_name)
        print("Successfully uploaded data to s3")
    except FileNotFoundError:
        print("Specified file was not found "+ file_path)
    
    