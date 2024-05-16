import os
from paramiko.ssh_exception import AuthenticationException
import paramiko
from tqdm import tqdm

class ModelNotFound(Exception):
    def __init__(self, error= "Cannot Load Model"):
        self.error = error
        super().__init__(self.error)

class SFTPWithProgressBar(paramiko.SFTPClient):
    def put(self, localpath, remotepath, callback=None, confirm=True):
        total_size = os.stat(localpath).st_size
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=remotepath) as pbar:
            def _callback(bytes_transferred, bytes_remaining):
                pbar.update(bytes_transferred - pbar.n)
                if callback:
                    callback(bytes_transferred, bytes_remaining)
            return super().put(localpath, remotepath, callback=_callback, confirm=confirm)
    
    # def get(self, localpath, remotepath, callback=None, confirm=True):
    #     total_size = os.stat(remotepath).st_size
    #     with tqdm(total=total_size, unit='B', unit_scale=True, desc=localpath) as pbar:
    #         def _callback(bytes_transferred, bytes_remaining):
    #             pbar.update(bytes_transferred - pbar.n)
    #             if callback:
    #                 callback(bytes_transferred, bytes_remaining)
    #         return super().get(remotepath, localpath, callback=_callback, confirm=confirm)
        
class EurBaseSDK():
    def get_model(self, filepath) ->str:
        extension = filepath.split(".")
        if extension[1] != "pt" and extension[1] != "tflite":
            print("Not supported file path")
            return ""
        
        if os.path.exists(filepath):
            print("Model file exist and ready to load")
            return filepath        
        else: 
            print("Model file is not available in the given path")
            return ""
    
    def connect_ssh_client(self, hostname, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=username, password=password)
            print("Connected to ", hostname)
            return ssh
        except AuthenticationException as err:
            print("Authentication to %s SSH failed - Invalid username or password" % hostname)
            exit(1)
        except TimeoutError as err:
            print("Connection Timeout Error: ", err)
            exit(1)
        except Exception as err:
            print("Error: %s" % err)
            exit(1)

    def download_from_remote(self, ssh_client, local_path, remote_path):
        print("Downloading file from {} to {}".format(remote_path, local_path))
        sftp_progress_bar = SFTPWithProgressBar.from_transport(ssh_client.get_transport())
        sftp_progress_bar.get(remote_path, local_path)
        print("File download successful")
    
    def download_file(self, ssh_client, local_path, remote_path):
        try:
            command = f"ls -t {remote_path} | grep predict"
            stdin, stdout, stderr = ssh_client.exec_command(f'{command}')
            op = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            if err != "":
                print("Error checking the prediction results: ", err)
                return
            if op != "":
                directories = op.split('\n')
                if not len(directories) or not directories[0]:
                    print(f"Prediction results not saved in {remote_path}")
                    return
                
                sftp = ssh_client.open_sftp()
                file = sftp.listdir_attr(remote_path + "/" + directories[0] + "/")[0].filename
                # print("File name: %s" % file)
                local_path = local_path + file
                remote_path = remote_path + "/" + directories[0] + "/" + file
                self.download_from_remote(ssh_client, local_path, remote_path)
            else:
                print("Error checking the prediction results: ", err)
                return
        except Exception as err:
            print("Error downloading file: ", err)
            ssh_client.close()
            exit(1)

    def upload_to_remote(self, ssh_client, local_path, remote_path):
        print("Uploading file {} to {}".format(local_path, remote_path))
        sftp_progress_bar = SFTPWithProgressBar.from_transport(ssh_client.get_transport())
        sftp_progress_bar.put(local_path, remote_path)
        print("File upload successful")

    def upload_file(self, ssh_client, local_path, remote_path, home_path):
        try:
            sftp = ssh_client.open_sftp()
            # print("Checking for file in {}".format(home_path))
            sftp.stat(remote_path)
            print("File already exists")
            upload = input("Do you want to upload it again (y/n)? ")
            while upload.lower() != 'y' and upload.lower() != 'n':
                print("Your response ('{}') was not one of the expected responses: y, n".format(upload))
                upload = input("Do you want to upload it again (y/n)? ")
            if upload == 'y':
                if not os.path.exists(local_path):
                    print("File '{}' does not exist".format(local_path))
                    print("Exiting...")
                    sftp.close()
                    ssh_client.close()
                    exit(1)
                self.upload_to_remote(ssh_client, local_path, remote_path)
            sftp.close()
        except IOError:
            print("File does not exist")
            self.upload_to_remote(ssh_client, local_path, remote_path)
            sftp.close()
        except Exception as err:
            print("Error uploading the file: ", err)
            sftp.close()
            ssh_client.close()
            exit(1)

    def execute_ssh_script(self, ssh_client, command):
        try:
            if command != "pwd":
                print("Executing script")
            stdin, stdout, stderr = ssh_client.exec_command(f'{command}')
            op = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            if op:
                return op
            if err:
                print(err)
                return ""
        except Exception as err:
            print("Error Executing the script: ", err)
            exit(1)
            
    def deploy_pytorch_model(self, scriptFile, modelFile, hostname, username, password):
        ssh_client = self.connect_ssh_client(hostname, username, password)
        home_path = self.execute_ssh_script(ssh_client, 'pwd')
        if home_path == "":
            exit(1)
        script_path = (f'{home_path}/{scriptFile}').replace('\n', "").strip()
        script_command = f'python3 -m venv mlsdk-venv && source ./mlsdk-venv/bin/activate && pip install eurmlsdk --upgrade && python3 {script_path} {modelFile}'
        execute_script = self.execute_ssh_script(ssh_client, script_command)
        if execute_script != "":
            print(execute_script)


    def deploy_model(self, scriptFile, local_path, hostname, username, password, modelFile):
        # Establish SSH connection
        ssh_client = self.connect_ssh_client(hostname, username, password)
        home_path = self.execute_ssh_script(ssh_client, 'pwd')
        if home_path == "":
            exit(1)
        remote_model_path = (f"{home_path}/{modelFile}").replace('\n', "").strip()
        script_path = (f'{home_path}/{scriptFile}').replace('\n', "").strip()
        print(f"Checking for model file in {home_path}")
        self.upload_file(ssh_client, local_path, remote_model_path, home_path)

        print("Choose between static dataset or live feed for prediction.")
        static = input("Static dataset (y/n)? ")
        static_path = ''
        while(static.lower() != 'y' and static.lower() != 'n'):
            print("Your response ('{}') was not one of the expected responses: y, n".format(static))
            static = input("Static dataset (y/n)? ")
        if static.lower() == 'y':
            dataset_path = input("Enter img/video path: ")
            dataset_file = dataset_path.split("/")[-1]
            remote_dataset_path = (f"{home_path}/{dataset_file}").replace('\n', "").strip()
            print(f"Checking for dataset file in {home_path}")
            self.upload_file(ssh_client, dataset_path, remote_dataset_path, home_path)
            feedType = 'static_feed'
            static_path = remote_dataset_path
        else:
            feedType = "live_feed"
            # exit(1)

        if feedType == "live_feed":
            script_command = f'python3 -m venv mlsdk-venv && source ./mlsdk-venv/bin/activate && pip install eurmlsdk --upgrade && python3 {script_path} {modelFile} {feedType}'
        else:
            script_command = f'python3 -m venv mlsdk-venv && source ./mlsdk-venv/bin/activate && pip install eurmlsdk --upgrade && python3 {script_path} {modelFile} {feedType} {static_path}'
        
        execute_script = self.execute_ssh_script(ssh_client, script_command)
        if execute_script != "":
            print(execute_script)
        
        # download prediction results to local
        predict_path = "/runs/detect"
        download_to = os.getcwd() + "/"
        download_from = (f"{home_path}{predict_path}").replace('\n', "").strip()
        # self.download_file(ssh_client, '', os.getcwd(), home_path + '/runs/detect/')
        self.download_file(ssh_client, download_to, download_from)
        ssh_client.close()
        exit()