from sys import argv,exit
import os
import logging
from .eur_sdk import ModelYolo

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info and warning logs
logging.getLogger('tensorflow').setLevel(logging.ERROR)  # Suppress TensorFlow warning logs
logging.getLogger('tensorflow.compiler.tf2tensorrt').setLevel(logging.ERROR)  # Suppress TensorFlow-TRT warning logs

def list_commands():
    print("Available commands in mlsdk package are:")
    print("  deploy <model path> <hostname> <username> <password> : Uploads the model file in the Raspberry pi")
    print("     <model path> : path to the model file")
    print("     <hostname>   : hostname to connect to Raspberry pi")
    print("     <username>   : username to connect to Raspberry pi")
    print("     <password>   : password to connect to Raspberry pi")
    print("  help | --h                : Lists all commands available in mlsdk package")
    print("  predict <model path> <dataset> : Predicts the labels and saves the predicted image")
    print("     <model path> : path to the model file")
    print("     <dataset>    : sample dataset image")
    print("  validate <model path>     : Validates the model and returns the metrics using default dataset")

def main(): 
    if len(argv) == 1:
        print("Model Zoo SDK")
        print("Package name: eurmlsdk")
        print("Version: 0.0.76")
        print("Run 'eurmlsdk help' or eurmlsdk --h to find the list of commands.")
        exit(1)

    command = argv[1]
    if command == "help" or command == "--h":
        list_commands()
        exit(1)
        
    elif command == "validate":
        if len(argv) <3:
            print("Give the model file name or file path")
        else:
            modelPath = argv[2]
            yoloSDK = ModelYolo()
            yoloSDK.validateModel(modelPath)
        exit(1)
        
    elif command == "predict":
        if len(argv) <3:
            print("Give the model file name or file file path")
            exit(1)
        elif len(argv) <4:
            print("Please provide atlest one data set of images")
            exit(1)                                                                                                                               
        else:
            modelPath = argv[2]
            predictData = argv[3]
            yoloSDK = ModelYolo()
            yoloSDK.predictModel(modelPath, predictData)
        exit(1)    
    
    elif command == "deploy":
        if len(argv) < 6:
            print("Missing required arguments")
            print("Usage: eurmlsdk deploy <model path> <hostname> <username> <password>")
        else:
            localPath = argv[2]
            hostname = argv[3]
            username = argv[4]
            password = argv[5]
            yoloSDK = ModelYolo()
            modelFile = localPath.split("/")[-1]
            yoloSDK.deployModel(localPath,  hostname, username, password ,  modelFile)
        exit(1)
        
    else:
        print("Unknown command. Please find the list of commands")
        list_commands()

if __name__ == "__main__":
    main()