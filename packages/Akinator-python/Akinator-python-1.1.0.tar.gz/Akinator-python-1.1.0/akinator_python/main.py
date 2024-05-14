import requests
from bs4 import BeautifulSoup

class AkinatorError(Exception):
    pass
class Akinator():
    def __init__(self,theme:str="characters",lang:str="jp",child_mode:bool=False) -> None:
        self.ENDPOINT=f"https://{lang}.akinator.com/"
        self.name=None
        self.description=None
        self.photo=None
        self.answer_id=None
        if theme=="characters":
            sid=1
        elif theme=="objects":
            sid=2
        elif theme=="animals":
            sid=14
        else:
            raise AkinatorError("the theme must be 'characters' / 'objects' / 'animals'")
        self.session=requests.session()
        self.json={
            "step":0,
            "progression":0.0,
            "sid":sid,
            "cm":child_mode,
            "answer":0,
        }

    def start_game(self):
        game=self.session.post(f"{self.ENDPOINT}game",json={"sid":self.json["sid"],"cm":self.json["cm"]}).text
        soup = BeautifulSoup(game,"html.parser")
        askSoundlike=soup.find(id="askSoundlike")
        question_label=soup.find(id="question-label").get_text()
        session_id=askSoundlike.find(id="session").get("value")
        signature_id=askSoundlike.find(id="signature").get("value")
        self.json["session"]=session_id
        self.json["signature"]=signature_id
        self.step=0
        self.progression=0.0
        self.question=question_label
        return question_label

    def post_answer(self,answer:str):
        if answer=="y":
            self.json["answer"]=0
        elif answer=="n":
            self.json["answer"]=1
        elif answer=="idk":
            self.json["answer"]=2
        elif answer=="p":
            self.json["answer"]=3
        elif answer=="pn":
            self.json["answer"]=4
        else:
            raise AkinatorError("the answer must be 'y' / 'n' / 'idk' / 'p' / 'pn'")
        try:
            progression=self.session.post(f"{self.ENDPOINT}answer",json=self.json)
            progression=progression.json()
            if progression["completion"]=="KO":
                raise AkinatorError("completion : KO")
            try:
                self.json["step"]=int(progression["step"])
                self.json["progression"]=float(progression["progression"])
                self.step=int(progression["step"])
                self.progression=float(progression["progression"])
                self.question=progression["question"]
                self.question_id=progression["question_id"]
            except:
                self.name=progression["name_proposition"]
                self.description=progression["description_proposition"]
                self.photo=["photo"]
                self.answer_id=progression["id_proposition"]
            return progression
        except:
            raise AkinatorError(progression.text)

    def go_back(self):
        if self.json["step"]==0:
            raise AkinatorError("it's first question")
        if "answer" in self.json:
            del self.json["answer"]
        try:
            goback=self.session.post(f"{self.ENDPOINT}cancel_answer",json=self.json)
            goback=goback.json()
            self.json["step"]=int(goback["step"])
            self.json["progression"]=float(goback["progression"])
            self.step=int(goback["step"])
            self.progression=float(goback["progression"])
            self.question=goback["question"]
            self.question_id=goback["question_id"]
            return goback
        except:
            raise AkinatorError(goback.text)

    def exclude(self):
        if "answer" in self.json:
            del self.json["answer"]
        try:
            exclude=self.session.post(f"{self.ENDPOINT}exclude",json=self.json)
            exclude=exclude.json()
            self.json["step"]=int(self.json["step"])
            self.json["progression"]=float(self.json["progression"])
            self.step=int(exclude["step"])
            self.progression=float(exclude["progression"])
            self.question=exclude["question"]
            self.question_id=exclude["question_id"]
            return exclude
        except:
            raise AkinatorError(exclude.text)