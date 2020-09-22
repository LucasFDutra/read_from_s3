import os

def sls_deploy():
    path_code_from = os.path.join('read_from_s3', 'src')
    path_code_to = os.path.join('.', 'src_tmp')
    os.system('cp -r '+path_code_from+' '+path_code_to)
    os.system('pip install -r requirements.txt -t '+path_code_to)
    os.system('cd '+ path_code_to +' && sls deploy')
    os.system('rm -r '+ path_code_to)