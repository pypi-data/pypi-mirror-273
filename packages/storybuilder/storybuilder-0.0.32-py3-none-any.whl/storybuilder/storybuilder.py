import json
import random
import os
import uuid
import copy
import re
import xml.etree.ElementTree as ET
from PIL import Image

from .storyprofiles import CHARACTER_FIGURE_ACCESSORY_KEYS, STORY_SCENARIO_STYLES
from .characterpostures import CHARACTER_FIGURES

DEFAULT_LANGUAGE="zh-CN"
LANGUAGE_ENG="en-US"
DEFAULT_NARRATOR="M"

class Story:

    @staticmethod
    def test(page):
        #path = os.path.join(page.storyId, "test.json")
        #directory = os.path.dirname(path)
        #if not os.path.exists(directory):
        #    os.makedirs(directory)
        with open("test.json", "w") as file:
            json.dump(
                page.export(), file, ensure_ascii=False, indent=4, sort_keys=False
            )

    @staticmethod
    def removeEmojis(text):
        emojiPattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U0001F926-\U0001F991"
                            "]+", flags = re.UNICODE)
        return re.sub(emojiPattern, '', text)

    @staticmethod
    def retrieveSvgSize(image_path):
        # Load the SVG file
        tree = ET.parse(image_path)
        root = tree.getroot()

        # Extract attributes from the <svg> tag
        width = root.get("width", 0)  # Get the width attribute
        height = root.get("height", 0)  # Get the height attribute
        viewBox = root.get("viewBox", "0, 0, 0, 0")  # Get the viewBox attribute

        split_pattern = r"[ ,]+"

        return [int(width), int(height)], [
            int(float(num)) for num in re.split(split_pattern, viewBox)
        ]

    @staticmethod
    def retrievePixelSize(image_path):
        # Open the image using the Python Imaging Library (PIL)
        image = Image.open(image_path)

        # Get the width and height of the image in pixels
        width, height = image.size

        # Return the width and height as a tuple
        return width, height

    @staticmethod
    def getImageSize(file_path):
        width = height = 0
        try:
            if ".svg" in file_path[-4:]:
                dim2, dim4 = Story.retrieveSvgSize(file_path)
                if dim2 == [0, 0]:
                    width = dim4[2]
                    height = dim4[3]
                else:
                    width = dim2[0]
                    height = dim2[1]
            elif (
                ".jpg" in file_path[-4:]
                or ".jpeg" in file_path[-5:]
                or ".png" in file_path[-4:]
                or ".gif" in file_path[-4:]
            ):
                width, height = Story.retrievePixelSize(file_path)
        except:
            print("retrieve image file size error:", file_path)
        return width, height

    def __init__(self, title, storyId=None, style="shinkai_makoto", mode="test", **kwargs):
        self.title = title
        self.storyId = storyId if storyId != None else uuid.uuid4()
        self.styles = STORY_SCENARIO_STYLES[style]
        self.locale = kwargs["locale"] if "locale" in kwargs else DEFAULT_LANGUAGE
        self.narrator = kwargs["narrator"] if "narrator" in kwargs else DEFAULT_NARRATOR
        self.pages = []
        assert mode.lower() in ("test", "production")
        self.mode=mode.lower()
        if self.mode == "production":
            self.posterPath = 'story/posters/'
            self.audioPath = 'story/audios/'
        else:
            self.posterPath = 'test/posters/'
            self.audioPath = 'test/audios/'

        self._cosUploader = kwargs["uploader"] if "uploader" in kwargs else None
        self._synthesizer = kwargs["synthesizer"] if "synthesizer" in kwargs else None

        self._defaultCharacters = CHARACTER_FIGURES

        print(f"New story Title: {title}, Id:", self.storyId)

    def getAudioPath(self, fileName):
        return os.path.join("/", self.audioPath, self.storyId, fileName)

    def getUserPostureId(
        self, actor, postures, keyScenario="stand", excludeAccessories=True
    ):
        if type(postures) is int:
            return postures
        if type(postures) is list and type(postures[0]) is int:
            return postures[0]
        if self._defaultCharacters == None:
            return 0

        currentActorFigures = self._defaultCharacters[actor]
        availableFigures = []
        for j, figure in enumerate(currentActorFigures):
            skip = False
            if excludeAccessories:
                for accessory in CHARACTER_FIGURE_ACCESSORY_KEYS:
                    if accessory in figure:
                        skip = True
            if skip:
                continue
            if keyScenario in figure and all(keyWord in figure for keyWord in postures):
                availableFigures.append({"index": j, "figure": figure})
        if len(availableFigures) > 0:
            return random.choice(availableFigures)["index"]
        else:
            return 0

    def appendPage(self, page):
        self.pages.append(page)

    def insertPage(self, pos, page):
        self.pages.insert(pos, page)

    def createPage(self, sceneType, **kwargs):
        if sceneType.lower() not in (
            "exam",
            "notes",
            "cover",
            "blackboard",
            "concentrak",
            "classroom",
        ):
            raise Exception(
                f"Invalid scenario type {sceneType}, must be one of ('exam', 'notes', 'cover', 'blackboard', 'concentrak', 'classroom')"
            )

        newPage = None

        if sceneType.lower() == "classroom":
            if "actor" not in kwargs:
                raise Exception(f'argument "actor" is required')
            if "postures" in kwargs:
                newPage = ClassroomPage(
                    self, kwargs["actor"], postures=kwargs["postures"]
                )
            else:
                newPage = ClassroomPage(self, kwargs["actor"])
        elif sceneType.lower() == "blackboard":
            if "source" not in kwargs:
                raise Exception(f'argument "source" is required')
            if "rect" in kwargs:
                newPage = BlackboardPage(self, kwargs["source"], rect=kwargs["rect"])
            else:
                newPage = BlackboardPage(self, kwargs["source"])
        elif sceneType.lower() == "exam":
            if "actor" not in kwargs:
                raise Exception(f'argument "actor" is required')
            if "postures" in kwargs:
                newPage = ExamPage(self, kwargs["actor"], postures=kwargs["postures"])
            else:
                newPage = ExamPage(self, kwargs["actor"])
        elif sceneType.lower() == "concentrak":
            if "text" not in kwargs:
                raise Exception(f'argument "text" is required')
            newPage = ConcentrakPage(self, kwargs["text"])
        elif sceneType.lower() == "cover":
            if "source" not in kwargs:
                raise Exception(f'argument "source" is required')
            if "rect" in kwargs:
                newPage = CoverPage(self, kwargs["source"], rect=kwargs["rect"])
            else:
                newPage = CoverPage(self, kwargs["source"])
        elif sceneType.lower() == "notes":
            if "actor" not in kwargs:
                raise Exception(f'argument "actor" is required')
            if "postures" in kwargs:
                newPage = NotesPage(self, kwargs["actor"], postures=kwargs["postures"])
            else:
                newPage = NotesPage(self, kwargs["actor"])

        if newPage != None:
            self.pages.append(newPage)

        return newPage

    def export(self):
        voices = [{"sound": "/story/audios/OurMusicBox - 24 Hour Coverage - intro.mp3"}]
        events = []
        for page in self.pages:
            pageObject = page.export(voiceOffset=len(voices), pageId=float(len(events)))
            voices = voices + [
                {"sound": entry["sound"]} for entry in pageObject["voices"]
            ]
            events = events + pageObject["events"]

        return {"voices": voices, "events": events}

    def exportScripts(self):
        voices = []
        for i, page in enumerate(self.pages):
            pageObject = page.export(voiceOffset=len(voices))
            voices = voices + [{"page": i, "voices": pageObject["voices"]}]

        return voices

    def exportAudios(self, localOutputPath, uploadToCos=False):
        if self._synthesizer:
            voices = self.exportScripts()
            for page in voices:
                for i, voice in enumerate(page["voices"]):
                    fileName = os.path.basename(voice["sound"])
                    character = voice["narrator"]
                    for language in voice["subscript"]:
                        subscript = (
                            voice["alternative"][language]
                            if ("alternative" in voice) and (language in voice["alternative"]) and (voice["alternative"][language] != None)
                            else voice["subscript"][language]
                        )
                        print(f'page/script id: {page["page"]}/{i}')
                        self._synthesizer.synthesizeFile(
                            character, self.removeEmojis(subscript), language, localOutputPath, fileName
                        )
                        localOutputFileName = os.path.join(localOutputPath, fileName)

                        if  self._cosUploader != None and uploadToCos:
                            _ = self._cosUploader.local2cos(localOutputFileName, self.storyId, self.audioPath)    
                        


class Page:
    def __init__(self, type, storyInstance):
        self.story = storyInstance
        self.narrator = storyInstance.narrator
        self.locale = storyInstance.locale
        self.type = type
        self.scene = {}
        self.board = {}
        self.objects = []
        self.interactions = []
        self.subscripts = []
        self.narrations = []
        self.actor = ""

    def _getUserId(self, actor):
        userId = -1
        for i, object in enumerate(self.objects):
            if object["name"].lower() == actor.lower():
                userId = i

        if userId == -1:
            self.objects.append({"name": actor})
            userId = len(self.objects) - 1
        return userId

    def updateScript(
        self, scriptId: int, text=None, actor=None, alternativeText=None, locale=None
    ):
        locale = self.locale if locale == None else locale
        if len(self.subscripts) > 0 and scriptId < len(self.subscripts):
            if text != None:
                self.subscripts[scriptId]["subscript"][locale] = text
            if actor != None:
                self.subscripts[scriptId]["narrator"] = actor
            if alternativeText != None:
                if "alternative" not in self.subscripts[scriptId]:
                    self.subscripts[scriptId]["alternative"] = {locale: alternativeText}
                else:
                    self.subscripts[scriptId]["alternative"][locale] = alternativeText
        else:
            scriptId = scriptId - len(self.subscript)
            if len(self.narrations) > 0 and scriptId < len(self.narrations):
                if text != None:
                    self.narrations[scriptId]["subscript"][locale] = text
                if actor != None:
                    self.narrations[scriptId]["narrator"] = actor
                if alternativeText != None:
                    self.narrations[scriptId]["alternative"][locale] = alternativeText

    def export(self, voiceOffset=0, pageId=0.0):
        raise NotImplementedError("Subclasses must implement export()")


##### 问答页面 #####
class ExamPage(Page):
    def __init__(self, storyInstance, actor, postures=["smilesay"]):
        super().__init__("exam", storyInstance)
        self.scene = self.story.styles["scenarios"]["exam"]
        self.actor = actor
        self.defaultObject = "exam"

        posture_list = (
            [postures]
            if (isinstance(postures, str) or isinstance(postures, int))
            else postures
        )
        self.interactions.append(
            {
                "start": "",
                "duration": "",
                "position": self.story.styles["positions"]["right-bottom"],
                "transform": "scale(1.5, 1.5)",
                "figure": self.story.getUserPostureId(
                    actor, posture_list, keyScenario="half"
                ),
                "type": "motion",
                "actor": self._getUserId(self.actor),
            }
        )
        self.questionInteractions = []
        self.questionSubscripts = []

    def setQuestion(self, question, options, answers=[], **kwargs):
        assert isinstance(options, list)
        answer_list = list(answers) if not isinstance(answers, list) else answers

        self.board = {
            "content": {
                "fontSize": kwargs["fontSize"] if "fontSize" in kwargs else 20,
                "fontColor": "white",
                "question": {self.locale: question},
                "options": {self.locale: options},
                "answer": {self.locale: answer_list},
                "colsPerRow": kwargs["colsPerRow"] if "colsPerRow" in kwargs else 1,
            },
            "type": "exam",
            "rect": kwargs["rect"] if "rect" in kwargs else [0, 0, 1, 1],
        }

        self.correctAnswerId = 0
        for i, option in enumerate(options):
            for entry in answer_list:
                if entry == option:
                    self.correctAnswerId += 2**i

        self.questionInteractions = []
        self.questionSubscripts = []

        # 添加初始化问题语音
        self.questionSubscripts.append(
            {
                "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                "subscript": {self.locale: question},
                "narrator": self.actor,
            }
        )
        # 初始化页面行为 onResult: -2
        self.questionInteractions.append(
            {
                "start": "",
                "duration": "",
                "onResult": -2,
                "content": {
                    "popup": 4,
                    "voice": len(self.questionSubscripts) - 1,
                    "text": "",
                },
                "actor": self._getUserId(self.defaultObject),
                "type": "talk",
            }
        )

        # 错误答案提示行为 onResult: -1
        self.questionInteractions.append(
            {
                "start": "",
                "duration": "",
                "onResult": -1,
                "content": {
                    "popup": 4,
                    "voice": -1,
                    "text": (
                        {self.locale: kwargs["alwaysTruePrompt"]}
                        if "alwaysTruePrompt" in kwargs
                        else {DEFAULT_LANGUAGE: "再想想", LANGUAGE_ENG: "Try again"}
                    ),
                },
                "actor": self._getUserId(self.defaultObject),
                "type": "talk",
            }
        )

        # 正确答案行为 onResult: 由所有正确答案id计算所得
        if self.correctAnswerId > 0:
            self.questionInteractions.append(
                {
                    "start": "",
                    "duration": "",
                    "onResult": self.correctAnswerId,
                    "content": {"popup": 2, "text": ""},
                    "actor": self._getUserId(self.defaultObject),
                    "type": "talk",
                }
            )

    def setFontSize(self, size):
        self.board["fontSize"] = size

    def setColsPerRow(self, colsPerRow):
        self.board["colsPerRow"] = colsPerRow

    def setRect(self, rect):
        self.board["rect"] = rect

    def setFontColor(self, color):
        self.board["fontColor"] = color

    def addImage(self, source, rect=[0, 0, 1, 1], uploadToCos=True, caption=None):
        assert len(rect) >= 4 and type(rect) is list
        if "contentList" not in self.board:
            self.board["contentList"] = []

        if  self.story._cosUploader != None and uploadToCos:
            source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)    

        self.board["contentList"].append(
            {
                "rect": rect,
                "image": {self.locale: source},
            }
        )
        if caption != None and len(caption) > 0:
            self.board["contentList"][-1]["caption"] = {self.locale: caption}

    def export(self, voiceOffset=0, pageId=0.0):
        outSubscripts = self.subscripts + self.questionSubscripts
        outInteractions = self.interactions + self.questionInteractions

        for i, interaction in enumerate(outInteractions):
            if (
                "content" in interaction
                and interaction["content"].get("voice", -1) >= 0
            ):
                outInteractions[i]["content"]["voice"] += voiceOffset

        return {
            "voices": outSubscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene,
                    "board": self.board,
                    "objects": self.objects,
                    "interactions": outInteractions,
                }
            ],
        }


##### 总结页面 #####
class NotesPage(Page):
    RESERVED_VOICE = -999

    def __init__(self, storyInstance, actor, postures=["smilesay"], endingEffect=True):
        super().__init__("notes", storyInstance)
        self.scene = self.story.styles["scenarios"]["notes"]["scene"]
        self.board = self.story.styles["scenarios"]["notes"]["board"]
        self.bullets = []
        self.actor = actor
        self.defaultObject = "ending"

        if endingEffect:
            self.interactions.append(
                {
                    "start": "",
                    "duration": "",
                    "content": {"text": "", "voice": self.RESERVED_VOICE},
                    "type": "talk",
                    "actor": self._getUserId(self.defaultObject),
                }
            )

        posture_list = (
            [postures]
            if (isinstance(postures, str) or isinstance(postures, int))
            else postures
        )
        self.interactions.insert(
            0,
            {
                "start": "",
                "duration": "",
                "position": self.story.styles["positions"]["right-bottom"],
                "transform": "scale(1.5, 1.5)",
                "figure": self.story.getUserPostureId(
                    actor, posture_list, keyScenario="half"
                ),
                "type": "motion",
                "actor": self._getUserId(actor),
            },
        )

    def addBullet(self, text):
        self.bullets.append(text)

    def export(self, voiceOffset=0, pageId=0.0):
        bullets_string = subscript = ""
        for bullet in self.bullets:
            bullets_string += f"<li>{bullet}</li>"
        subscript = "<break time=\"1500ms\"/>".join(self.bullets)

        outBoard = copy.deepcopy(self.board)
        outBoard["content"]["html"] = {
            self.locale: outBoard["content"]["html"].format(bullets_string)
        }

        outSubscripts = copy.deepcopy(self.subscripts)
        outSubscripts.append(
            {
                "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                "subscript": {self.locale: subscript},
                "narrator": self.actor,
            }
        )

        outInteractions = copy.deepcopy(self.interactions)
        outInteractions.insert(
            len(outInteractions) - 1,
            {
                "start": "",
                "duration": "",
                "content": {"popup": 4, "voice": len(outSubscripts) - 1, "text": ""},
                "type": "talk",
                "actor": self._getUserId(self.defaultObject),
            },
        )
        for i, interaction in enumerate(outInteractions):
            if "content" in interaction:
                if interaction["content"].get("voice", -1) >= 0:
                    outInteractions[i]["content"]["voice"] += voiceOffset
                elif interaction["content"].get("voice", -1) == self.RESERVED_VOICE:
                    outInteractions[i]["content"]["voice"] = 0

        return {
            "voices": outSubscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene,
                    "board": outBoard,
                    "objects": self.objects,
                    "interactions": outInteractions,
                }
            ],
        }


##### 黑板页面 #####
class BlackboardPage(Page):
    def __init__(self, storyInstance, source, rect=[0, 0, 1, 1], uploadToCos=True):
        assert len(rect) >= 4 and type(rect) is list
        super().__init__("blackboard", storyInstance)
        self.scene = self.story.styles["scenarios"]["blackboard"]

        if  self.story._cosUploader != None and uploadToCos:
            source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)

        self.board = {"content": {"image": {self.locale: source}}, "rect": rect}

    def addNarration(self, text, narrator=None, alternativeText=None):
        if alternativeText != None:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                    "subscript": {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                }
            )
        else:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                    "subscript": {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                    "alternative": {self.locale: alternativeText},
                }
            )
        self.interactions.append(
            {
                "start": "",
                "duration": "auto",
                "content": {
                    "popup": 4,
                    "voice": len(self.subscripts) - 1,
                    "text": {self.locale: text},
                },
                "actor": self._getUserId(
                    narrator if narrator != None else self.narrator
                ),
                "type": "talk",
            }
        )

    def updateImage(self, source=None, rect=None, locale=None, uploadToCos=True):
        if source != None:
            if  self.story._cosUploader != None and uploadToCos:
                source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)
                
            self.board["content"]["image"][
                locale if locale != None else self.locale
            ] = source
        if rect != None:
            self.board["content"]["rect"] = rect

    def export(self, voiceOffset=0, pageId=0.0):
        outInteractions = copy.deepcopy(self.interactions)
        for i, interaction in enumerate(outInteractions):
            if (
                "content" in interaction
                and interaction["content"].get("voice", -1) >= 0
            ):
                outInteractions[i]["content"]["voice"] += voiceOffset
        return {
            "voices": self.subscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene,
                    "board": self.board,
                    "objects": self.objects,
                    "interactions": outInteractions,
                }
            ],
        }


##### 概念页面 #####
class ConcentrakPage(Page):
    def __init__(self, storyInstance, text):
        super().__init__("concentrak", storyInstance)
        self.scene = self.story.styles["scenarios"]["concentrak"]
        self.defaultObject = "concentrak"
        self.interactions.append(
            {
                "start": "",
                "duration": "",
                "actor": self._getUserId(self.defaultObject),
                "content": {"popup": 6, "text": {self.locale: text}},
            }
        )

    def addNarration(self, text, narrator=None, alternativeText=None):
        if alternativeText != None:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                    "subscript": {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                }
            )
        else:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                    "subscript": {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                    "alternative": {self.locale: alternativeText},
                }
            )
        self.interactions.append(
            {
                "start": "",
                "duration": "auto",
                "content": {
                    "popup": 4,
                    "voice": len(self.subscripts) - 1,
                    "text": {self.locale: text},
                },
                "actor": self._getUserId(
                    narrator if narrator != None else self.narrator
                ),
                "type": "talk",
            }
        )

    def export(self, voiceOffset=0, pageId=0.0):
        outInteractions = copy.deepcopy(self.interactions)
        for i, interaction in enumerate(outInteractions):
            if (
                "content" in interaction
                and interaction["content"].get("voice", -1) >= 0
            ):
                outInteractions[i]["content"]["voice"] += voiceOffset
        return {
            "voices": self.subscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene,
                    "board": self.board,
                    "objects": self.objects,
                    "interactions": outInteractions,
                }
            ],
        }


##### 首页页面 #####
class CoverPage(Page):
    def __init__(self, storyInstance, source, rect=[0, 0, 1, 1], uploadToCos=True):
        assert len(rect) >= 4 and type(rect) is list
        super().__init__("cover", storyInstance)
        self.scene = self.story.styles["scenarios"]["cover"]

        if self.story._cosUploader != None and uploadToCos:
            source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)

        self.board = {"content": {"image": {self.locale: source}}, "rect": rect}

    def addNarration(self, text, narrator=None, alternativeText=None):
        if alternativeText != None:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                    "subscript": {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                }
            )
        else:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                    "subscript": {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                    "alternative": {self.locale: alternativeText},
                }
            )
        self.interactions.append(
            {
                "start": "",
                "duration": "",
                "content": {
                    "popup": 4,
                    "voice": len(self.subscripts) - 1,
                    "text": {self.locale: text},
                },
                "actor": self._getUserId(
                    narrator if narrator != None else self.narrator
                ),
                "type": "talk",
            }
        )

    def export(self, voiceOffset=0, pageId=0.0):
        outInteractions = copy.deepcopy(self.interactions)
        for i, interaction in enumerate(outInteractions):
            if (
                "content" in interaction
                and interaction["content"].get("voice", -1) >= 0
            ):
                outInteractions[i]["content"]["voice"] += voiceOffset
        return {
            "voices": self.subscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene,
                    "board": self.board,
                    "objects": self.objects,
                    "interactions": self.interactions,
                }
            ],
        }


##### 教室页面 #####
class ClassroomPage(Page):
    def __init__(self, storyInstance, actor, postures=["smilesay"]):
        super().__init__("classroom", storyInstance)
        self.scene = self.story.styles["scenarios"]["classroom"]
        self.narrations = {"subscripts": [], "interactions": []}

        posture_list = (
            [postures]
            if (isinstance(postures, str) or isinstance(postures, int))
            else postures
        )
        self.subscripts.insert(
            0,
            {
                "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                "subscript": {self.locale: ""},
                "narrator": actor,
            },
        )
        self.interactions.insert(
            0,
            {
                "start": "",
                "duration": "",
                "content": {
                    "popup": self.story.styles["popup"],
                    "voice": 0,
                    "text": {self.locale: ""},
                },
                "figure": self.story.getUserPostureId(
                    actor, posture_list, keyScenario="-stand-"
                ),
                "position": self.story.styles["positions"][
                    "left" if actor == "boy" else "right"
                ],
                "transform": f'scale({self.story.styles["scale"]}, {self.story.styles["scale"]})',
                "type": "talk",
                "actor": self._getUserId(actor),
            },
        )
        self.actor = actor
        self.hasImage = False

    def setVoice(self, text, alternativeText=None):
        self.subscripts[0]["subscript"][self.locale] = text
        if alternativeText != None:
            self.subscripts[0]["alternativeText"][self.locale] = alternativeText
        self.interactions[0]["content"]["text"][self.locale] = text

    def setImage(self, source, rect=[0.2, 0.2, 400, 400], autoFit=True, uploadToCos=True, **kwargs):
        assert len(rect) >= 4 and type(rect) is list
        width, height = Story.getImageSize(source)
        assert width > 0 and height > 0
        assert rect[2] > 0 and rect[3] > 0

        if autoFit:
            # image is wider in ratio
            if width / height > rect[2] / rect[3]:
                height = round(rect[2] * height / width, 3)
                width = rect[2]
            # vice versa, rect is wider in ratio
            else:
                width = round(rect[3] * width / height, 3)
                height = rect[3]
            rect[2] = width
            rect[3] = height

        if autoFit and self.actor == "boy":
            if rect[2] > 1.0:
                rect[0] = round(0.9 - rect[2]/960.0, 3)
            elif rect[2] < 1.0:
                rect[0] = 0.9 - rect[2]

        if self.story._cosUploader != None and uploadToCos:
            source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)

        self.board = {
            "content": {
                "caption": kwargs["caption"] if "caption" in kwargs else "",
                "fontSize": kwargs["fontSize"] if "fontSize" in kwargs else "24px",
                "fontColor": kwargs["fontColor"] if "fontColor" in kwargs else "white",
                "image": {self.locale: source},
                "magnify": True,
                "border": self.story.styles["frame"],
            },
            "rect": rect,
        }
        self.hasImage = True

    def setVideo(self, source, autoFit=True, rect=[0.1, 0.1, 640, 360], **kwargs):
        assert len(rect) >= 4 and type(rect) is list

        if autoFit and self.actor == "boy":
            if rect[2] > 1.0:
                rect[0] = round(0.9 - rect[2]/0.9, 3)
            elif rect[2] < 1.0:
                rect[0] = 0.9 - rect[2]

        self.board = {
            "content": {
                "caption": kwargs["caption"] if "caption" in kwargs else "",
                "fontSize": kwargs["fontSize"] if "fontSize" in kwargs else "24px",
                "fontColor": kwargs["fontColor"] if "fontColor" in kwargs else "white",
                "src": {self.locale: source},
                "border": self.story.styles["frame"],
            },
            "rect": rect,
        }
        if "videoType" in kwargs:
            self.board["content"]["videoType"] = kwargs["videoType"].lower()
        self.hasImage = True

    def addNarration(self, text, narrator=None, alternativeText=None):
        if alternativeText != None:
            self.narrations["subscripts"].append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                    "subscript": {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                }
            )
        else:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3"),
                    "subscript": {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                    "alternative": {self.locale: alternativeText},
                }
            )
        self.narrations["interactions"].append(
            {
                "start": "",
                "duration": "auto",
                "content": {
                    "popup": 4,
                    "voice": len(self.narrations["subscripts"]) - 1,
                    "text": {self.locale: text},
                },
                "onPoster": 1,
                "actor": self._getUserId(
                    narrator if narrator != None else self.narrator
                ),
                "type": "talk",
            }
        )

    def export(self, voiceOffset=0, pageId=0.0):
        outSubscripts = copy.deepcopy(self.subscripts)
        outInteractions = copy.deepcopy(self.interactions)
        outNarrations = copy.deepcopy(self.narrations)

        if self.hasImage:
            for i, interaction in enumerate(outInteractions):
                if interaction["type"] != "motion":
                    outInteractions[i]["duration"] = "auto"
                    outInteractions[i]["content"]["popup"] = 4

        outSubscripts = outSubscripts + outNarrations["subscripts"]
        narrationOffset = len(outSubscripts)
        for i, interaction in enumerate(outNarrations["interactions"]):
            outNarrations["interactions"][i]["content"]["voice"] += narrationOffset
            outInteractions.append(outNarrations["interactions"][i])

        for j, interaction in enumerate(outInteractions):
            if (
                "content" in interaction
                and interaction["content"].get("voice", -1) >= 0
            ):
                outInteractions[j]["content"]["voice"] += voiceOffset
        return {
            "voices": outSubscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene,
                    "board": self.board,
                    "objects": self.objects,
                    "interactions": outInteractions,
                }
            ],
        }
