from ultralytics import YOLO
from .eur_sdk import EurBaseSDK, ModelNotFound

class ModelYolo(EurBaseSDK):
    def load_model(self, modelPath) -> YOLO:
        modelFile = self.get_model(modelPath)
        if modelFile != "":
            model = YOLO(modelPath)
            return model 
        else:
            raise ModelNotFound()
        
    def predict_model(self, pathArg, dataSet):
        try:
            model = self.load_model(pathArg)
            print("Prediction started.....")
            results = model(dataSet,stream=True)
            print(f"Prediction results: {results}")
            # model.predict(dataSet, save=True)
        except ModelNotFound as err:
            print("Error :", err)
            exit(1)
        except Exception as err:
            print("Error in Prediction :", err)
            exit(1)

    def validate_model(self, pathArg, task):
        try: 
            model = self.load_model(pathArg)
            print("Validation started........")
            dataset = {
                "seg" : "coco8-seg.yaml",
                "pose" : "coco8-pose.yaml",
            }
            metrics = model.val(data=dataset.get(task, "coco8.yaml"))
            print("Validated Metrics", metrics)
        except ModelNotFound as err:
            print("Error :", err)
            exit(1)