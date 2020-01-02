from imageai.Detection.Custom import CustomObjectDetection

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("detection_model-ex-046--loss-8.848.h5")
detector.setJsonPath("detection1_config.json")
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="input.jpg", output_image_path="output.jpg")
for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])

