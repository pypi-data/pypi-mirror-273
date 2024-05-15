import os
import pysftp
import paramiko


def recursive_list(sftp, remote_path):
    """Recursively list all directories and files under remote_path"""
    file_structure = {}
    for entry in sftp.listdir_attr(remote_path):
        full_path = os.path.join(remote_path, entry.filename)
        if entry.st_mode & 0o40000:  # if directory
            file_structure[entry.filename] = recursive_list(sftp, full_path)
        else:  # if file
            file_structure[entry.filename] = 'file'
    return file_structure

def sftp_connect(host, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy)  # Warn if host key not in known_hosts
        
        ssh.connect(host, username=username, password=password)
        
        with ssh.open_sftp() as sftp:
            file_structure = recursive_list(sftp, '.')
        
        ssh.close()
        return file_structure
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    


    
