from sys import argv,exit
import os
import logging
from .yolo import ModelYolo
from .pytorch import ModelPytorch

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info and warning logs
logging.getLogger('tensorflow').setLevel(logging.ERROR)  # Suppress TensorFlow warning logs
logging.getLogger('tensorflow.compiler.tf2tensorrt').setLevel(logging.ERROR)  # Suppress TensorFlow-TRT warning logs

def list_commands():
    print("Available commands in eurmlsdk package are:")
    print("  deploy <model type> <model path> <hostname> <username> <password> : Uploads the model file and executes remote script")
    print("  help | --h                                           : Lists all commands available in eurmlsdk package")
    print("  predict <model path> <dataset path>                  : Predicts the labels and saves the predicted result")
    print("  validate <task> <model path>                         : Validates the model and returns the metrics using default dataset")
    print("  pt-predict <model name>                              : Predicts the labels and prints the predicted results")
    print("  pt-list-model                                        : Lists all the pytorch models available")
    print("  pt-validate <model name>                             : Validates the model and prints the metrics")
    print(" ")
    print("Options:")
    print(" <dataset path> : Image or Video path")
    print(" <hostname>     : Remote Server hostname")
    print(" <model path>   : Model file path")
    print(" <model type>   : Model type - 'yolo' or 'pt'")
    print(" <password>     : Remote Server password")
    print(" <task>         : Validation task - 'seg' or 'pose' or 'detect' or 'classify'")
    print(" <username>     : Remote Server username")

def main():
    commands_list = ['deploy','help','--h','predict','validate', 'pt-predict', 'pt-validate', 'pt-list-model']
    try:
        argLen = len(argv)
        if argLen == 1:
            print("Model Zoo SDK")
            print("Package name: eurmlsdk")
            print("Version: 0.1.0")
            print("Run 'eurmlsdk help' or eurmlsdk --h to find the list of commands.")
            exit()

        command = argv[1]
        if command not in commands_list:
            print("Unknown command. Please find the list of commands")
            list_commands()
            exit()

        if command == "help" or command == "--h":
            list_commands()

        elif command =="pt-list-model":
            model_list = ['AlexNet','ConvNeXt','DenseNet','EfficientNet','EfficientNetV2','GoogLeNet','Inception V3','MaxVit','MNASNet','MobileNet V2', 'MobileNet V3','RegNet','ResNet','ResNeXt','ShuffleNet V2','SqueezeNet','SwinTransformer','VGG','VisionTransformer','Wide ResNet']
            for model in model_list:
                print(model)

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

        elif command == "pt-predict":
            if argLen <3 :
                print("Missing required arguments")
                print("<model_path> <dataset_path>")
                exit(1)
            else:
                model_path = argv[2]
                pyTorchSDK = ModelPytorch()
                class_result = pyTorchSDK.predict_model(model_path)
                pyTorchSDK.get_predicted_results(class_result)

        elif command == "pt-validate":
            if argLen <3 :
                print("Missing required arguments")
                print("<model_path> <dataset_path>")
                exit(1)
            else:
                model_path = argv[2]
                pyTorchSDK = ModelPytorch()
                validate_result = pyTorchSDK.validate_model(model_path)
                print("Validation result", validate_result)

        elif command == "deploy":
            if argLen < 7:
                print("Missing required arguments")
                print("Usage: eurmlsdk deploy <model type> <model path> <hostname> <username> <password>")
                exit(1)
            if len(argv) > 7:
                print("Too many arguments")
                print("Usage: eurmlsdk deploy <model type> <model path> <hostname> <username> <password>")
                exit(1)
            localPath = argv[3]
            hostname = argv[4]
            username = argv[5]
            password = argv[6]
            modelFile = localPath.split("/")[-1]
            if argv[2] == "yolo":
                modelSDK = ModelYolo()
                scriptPath = "hello.py"
                modelSDK.deploy_model(scriptPath, localPath,  hostname, username, password , modelFile) 
            elif argv[2] == "pt":
                modelSDK = ModelPytorch()
                scriptPath = "pytorch.py"
                modelSDK.deploy_pytorch_model(scriptPath, modelFile, hostname, username, password)
        else:
            print("Unknown command. Please find the list of commands")
            list_commands()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(130)

if __name__ == "__main__":
    exit(main())