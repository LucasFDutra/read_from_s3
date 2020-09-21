import os

def sls_deploy():
    files_in_folder = os.listdir('read_from_s3/src')
    os.system('pip install -r requirements.txt -t ./read_from_s3/src')
    os.system('cd read_from_s3/src && sls deploy')
    files_in_folder_after = os.listdir('read_from_s3/src')
    
    for f in files_in_folder_after:
        if (not f in files_in_folder):
            os.system('rm -r read_from_s3/src/'+f)