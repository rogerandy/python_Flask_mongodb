# 連結MongoDB初始資料
from flask import *
import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://yayv332211:MWfQTzJdPMr27Faa@cluster0.grk2rlh.mongodb.net/?retryWrites=true&w=majority")

db = client.data
collection = db.member  # Correct indentation

print("成功")
# 初始API資料
app = Flask(__name__, static_folder="static", static_url_path="/")

# 密鑰
app.secret_key = "hello_roger"


# /app畫面
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html")
    else:
        return redirect("/")


@app.route("/error")
def error():
    msg = request.args.get("msg", "發生錯誤,請聯繫roger")
    return render_template("error.html", message=msg)


@app.route("/signup", methods=["POST"])
def sign_up():
    # 從前端接收資料
    nickname = request.form["nickname"]
    mail = request.form["mail"]
    password = request.form["password"]
    # 接收資料與資料庫作互動
    # error
    result = collection.find_one({"mail": mail})

    if result != None:
        return redirect("/error?msg=錯誤訊息,信箱被註冊")

    collection.insert_one({
        "nickname": nickname,
        "mail": mail,
        "password": password
    })
    return redirect("/")


@app.route("/signin", methods=["POST"])
def sign_in():
    mail = request.form["mail"]
    password = request.form["password"]
    result = collection.find_one({
        "$and": [{
            "mail": mail},
            {"password": password}]
    })
    # 找不到資料,須入錯誤 倒回錯誤畫面
    if result == None:
        return redirect("/error?msg=帳號密碼輸入錯誤")
    session["nickname"] = result["nickname"]
    return redirect("/member")

# 設計一個sign out的網頁 delete輸入裡面的訊息(登出後)


@app.route("/signout")
def signout():
    del session["nickname"]
    return redirect("/")


app.run()
