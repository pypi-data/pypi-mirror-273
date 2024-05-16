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
            results = model(dataSet,stream=True,save=True)
            print(f"Prediction results: {results}")
            for result in results:
                boxes = result.boxes  # Boxes object for bounding box outputs
                masks = result.masks  # Masks object for segmentation masks outputs
                keypoints = result.keypoints  # Keypoints object for pose outputs
                probs = result.probs  # Probs object for classification outputs
                obb = result.obb  # Oriented boxes object for OBB outputs
                # result.show()  # display to screen
                # result.save(filename='result.jpg')  # save to disk
                print(boxes)
                print(masks)
                print(keypoints)
                print(probs)
                print(obb)
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