from sys import argv,exit
import os
import logging
from .yolo import ModelYolo

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info and warning logs
logging.getLogger('tensorflow').setLevel(logging.ERROR)  # Suppress TensorFlow warning logs
logging.getLogger('tensorflow.compiler.tf2tensorrt').setLevel(logging.ERROR)  # Suppress TensorFlow-TRT warning logs

def list_commands():
    print("Available commands in eurmlsdk package are:")
    print("  deploy <model path> <hostname> <username> <password> : Uploads the model file and executes remote script")
    print("  help | --h                                           : Lists all commands available in eurmlsdk package")
    print("  predict <model path> <dataset path>                  : Predicts the labels and saves the predicted result")
    print("  validate <task> <model path>                         : Validates the model and returns the metrics using default dataset")
    print(" ")
    print("Options:")
    print(" <dataset path> : Image or Video path")
    print(" <hostname>     : Remote Server hostname")
    print(" <model path>   : Model file path")
    print(" <password>     : Remote Server password")
    print(" <task>         : Validation task - 'seg' or 'pose' or 'detect' or 'classify'")
    print(" <username>     : Remote Server username")

def main():
    commands_list = ['deploy','help','--h','predict','validate']
    try:
        argLen = len(argv)
        if argLen == 1:
            print("Model Zoo SDK")
            print("Package name: eurmlsdk")
            print("Version: 0.0.84")
            print("Run 'eurmlsdk help' or eurmlsdk --h to find the list of commands.")
            exit()

        command = argv[1]
        if command not in commands_list:
            print("Unknown command. Please find the list of commands")
            list_commands()
            exit()

        if command == "help" or command == "--h":
            list_commands()
        elif command == "validate":
            taskList = ["seg", "pose", "classify", "detect"]
            if argLen < 4:
                print("Missing required arguments")
                print("Usage: eurmlsdk validate <task> <model path>")
                exit(1)
            if argLen > 4:
                print("Too many arguments")
                print("Usage: eurmlsdk validate <task> <model path>")
                exit(1)
            if argv[2] not in taskList:
                print("Please provide valid task for validation")
                exit(1)
            modelPath = argv[3]
            task = argv[2]
            yoloSDK = ModelYolo()
            yoloSDK.validate_model(modelPath, task)
        elif command == "predict":
            if argLen < 4:
                print("Missing required arguments")
                print("Usage: eurmlsdk predict <model path> <dataset path>")
                exit(1)
            if argLen > 4:
                print("Too many arguments")
                print("Usage: eurmlsdk predict <model path> <dataset path>")
                exit(1)
            modelPath = argv[2]
            predictData = argv[3]
            yoloSDK = ModelYolo()
            yoloSDK.predict_model(modelPath, predictData)
        elif command == "deploy":
            if argLen < 6:
                print("Missing required arguments")
                print("Usage: eurmlsdk deploy <model path> <hostname> <username> <password>")
                exit(1)
            if len(argv) > 6:
                print("Too many arguments")
                print("Usage: eurmlsdk deploy <model path> <hostname> <username> <password>")
                exit(1)
            localPath = argv[2]
            hostname = argv[3]
            username = argv[4]
            password = argv[5]
            yoloSDK = ModelYolo()
            modelFile = localPath.split("/")[-1]
            yoloSDK.deploy_model(localPath,  hostname, username, password ,  modelFile) 
        else:
            print("Unknown command. Please find the list of commands")
            list_commands()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(130)

if __name__ == "__main__":
    exit(main())