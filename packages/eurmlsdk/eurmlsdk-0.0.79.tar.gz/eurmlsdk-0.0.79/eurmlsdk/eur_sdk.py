import os
from ultralytics import YOLO
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
        
class EurBaseSDK():  
    def getModel(self, filepath) ->str:
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

    def uploadToRemote(self, ssh_client, local_path, remote_path):
        print("Uploading model {} to {}".format(local_path, remote_path))
        sftp_progress_bar = SFTPWithProgressBar.from_transport(ssh_client.get_transport())
        sftp_progress_bar.put(local_path, remote_path)
        print("Model upload successful")

    def uploadModel(self, ssh_client, local_path, remote_path, home_path):
        try:
            sftp = ssh_client.open_sftp()
            sftp.chdir(home_path)
            sftp.stat(remote_path)
            print('Model File {} already exists'.format(remote_path.split("/")[-1]))
            upload = input('Do you want to upload it again (y/n)? ')
            while upload.lower() != 'y' and upload.lower() != 'n':
                print("Your response ('{}') was not one of the expected responses: y, n".format(upload))
                upload = input('Do you want to upload it again (y/n)? ')
            if upload == 'y':
                self.uploadToRemote(ssh_client, local_path, remote_path)
            sftp.close()
        except IOError:
            self.uploadToRemote(ssh_client, local_path, remote_path)
            sftp.close()
            exit(1)
        except Exception as err:
            print("Error uploading the model file: ", err)
            exit(1)

    def execute_ssh_script(self, ssh_client, command):
        try:
            print("Executing script")
            stdin, stdout, stderr = ssh_client.exec_command(f'{command}')
            op = stdout.read().decode('utf-8')
            err = stdout.read().decode('utf-8')
            if op:
                return op
            if err:
                print(err)
                return ""
        except Exception as err:
            print("Error Executing the script: ", err)
            exit(1)
              
    def deployModel(self, local_path, hostname, username, password, modelFile):
        # Establish SSH connection
        ssh_client = self.connect_ssh_client(hostname, username, password)
        home_path = self.execute_ssh_script(ssh_client, 'pwd')
        if home_path != "":
            remote_path = (f"{home_path}/{modelFile}").replace('\n', "").strip()
            script_path = (f'{home_path}/hello.py').replace('\n', "").strip()
            self.uploadModel(ssh_client, local_path, remote_path, home_path)
            script_command = f'python3 -m venv mlsdk-venv && source ./mlsdk-venv/bin/activate && pip install eurmlsdk --upgrade && python3 {script_path} {modelFile}'
            # self.execute_script(ssh_client, script_path , modelFile)
            execute_script = self.execute_ssh_script(ssh_client, script_command)
            if execute_script != "":
                print(execute_script)
            # Close SSH connection
            ssh_client.close()
        exit(1)

class ModelYolo(EurBaseSDK):
    def loadModel(self, modelPath) -> YOLO:
        modelFile = self.getModel(modelPath)
        if modelFile != "":
            model = YOLO(modelPath)
            return model 
        else:
            raise ModelNotFound()
        
    def predictModel(self, pathArg, dataSet):
        data = []
        data.append(dataSet)
        try:
            model = self.loadModel(pathArg)
            print("Prediction started.....")
            model.predict(dataSet, save=True)
        except ModelNotFound as err:
            print("Error :", err)
            exit(1)
        except Exception as err:
            print("Error in Prediction :", err)
            exit(1)

    def validateModel(self, pathArg):
        try: 
            model = self.loadModel(pathArg)
            print("Validation started........")
            metrics = model.val(data='coco8.yaml')
            print("Validated Metrics", metrics)
        except ModelNotFound as err:
            print("Error :", err)
            exit(1)