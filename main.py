from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Utils import ConvertChinpo 
import base64
from io import BytesIO
from PIL import Image
from pydantic import BaseModel
from Utils import SearchChinpoTweet

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://192.168.10.14:3000",
    "http://192.168.10.14",
    "https://chinpo-festival-front.vercel.app",
] #通信するreactなどのアプリのURLを記載

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #クロスオリジンを許可するオリジンのリストを配列で指定する。
    allow_credentials=True, #Cookieの共有を許可するかどうか。デフォルトはFalse。
    allow_methods=["*"], #許可するHTTPメソッドを指定する。デフォルトはGET。アスタリスク( * )にすることで全てのHTTPメソッドを許可する。
    allow_headers=["*"], #オリジン間リクエストでサポートするHTTPリクエストヘッダーのリスト。デフォルトは [] 。['*']を使用して、すべてのヘッダーを許可できる。
)

# リクエストボディで引数をもらう場合、Jsonに対応した項目をクラスとして定義しておく
class ChinpoImageItem(BaseModel):
    base64_image_string: str

@app.get("/getRecentChinpo") 
def GetRecentChinpo():
    results = SearchChinpoTweet.search_tweet()
    return results

@app.post("/chinpo") 
def letsChinpo(item: ChinpoImageItem): # リクエストボディで送る場合    
    base64_image_string = item.base64_image_string
    
    image = Image.open(BytesIO(base64.b64decode(base64_image_string.split(",")[1])))

    chinpo_image = ConvertChinpo.paste_chinpo(image)
    
    buff = BytesIO()
    chinpo_image.save(buff, format="JPEG")
    base64_chinpo_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    
    #自分でJSONを組み立てて返してもOK
    data = {"base64_image_string": base64_chinpo_image_string, "name": "chinpo-image"}
    return data