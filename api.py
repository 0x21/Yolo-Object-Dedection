from imageai.Detection.Custom import CustomObjectDetection
import json
import requests
import imageio
class api:
    def __init__(self):
        self.detector = CustomObjectDetection()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("detection_model-ex-046--loss-8.848.h5")
        self.detector.setJsonPath("detection1_config.json")
        self.detector.loadModel()
        self.username="****"
        self.password="****"
        self.data={
                "kadi" : f"{self.username}",
                "sifre" : f"{self.password}"
                  }
        self.baseurl="***" #http://blabla
        self.signin()
    def signin(self):
        self.s=requests.session()
        self.r=self.s.post(f"{self.baseurl}/api/giris",json=self.data)
        if self.r.status_code==200:
            self.getimageList()
        elif self.r.status_code==400:
            print("Kullanıcı adı veya parola geçersiz")
        else:
            print(self.r.status_code+"*???*"+self.r.content)

            
    def getimageList(self):
         self.jsonReq=self.s.get(f"{self.baseurl}/api/frame_listesi")
         with open("frame_list.txt","w") as fp:
             fp.write(self.jsonReq.text)
         print("json indi")
         self.sendimageData()
         
    def sendimageData(self):
        json_file = open('frame_list.txt')
        data = json.load(json_file)
        for do in data:
            a={"frame_id":do['frame_id'],"objeler":[]}
            img=imageio.imread(f"http://{do['frame_link']}")
            detections = self.detector.detectObjectsFromImage(input_type="array",input_image=img,output_type="array",thread_safe=True)
            for detection in detections[1]:
                a["objeler"].append({"tur":detection["name"],"x1":detection["box_points"][0],"y1":detection["box_points"][1],"x2":detection["box_points"][2],"y2":detection["box_points"][3]})   

            self.true=self.s.post(f"{self.baseurl}/api/cevap_gonder",json=a)
            print(f"[+] http://{do['frame_link']} "+str(self.true.status_code))
            a["objeler"].clear()
        
        print("Tüm resimler okundu")
        self.logout()

    def logout(self):
        self.s.get(f"{self.baseurl}/api/cikis")

api()
        