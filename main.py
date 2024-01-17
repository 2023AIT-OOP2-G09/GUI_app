from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

from module.add import schedule_duplicate

app = Flask(__name__)


# 最初のカレンダーのページ
@app.route("/")
def index():
    # ここにカレンダー表示のtemplateを返す
    return render_template("index.html")


# 予定追加のページ
@app.route("/add")
def add():
    # 予定追加のtemplateを返す
    return render_template("AddSchedule.html")


# データ追加工程
@app.route("/add/to", methods=["GET", "POST"])
def address_get():
    if request.method == "POST":
        try:
            # 検索パラメータの取得
            p_date = request.form.get("date")
            print(p_date)
            p_schedule = request.form.get("schedule")
            p_time = request.args.get("tm")

            # データを分ける
            if p_date is not None:
                p_date_obje = datetime.strptime(p_date, "%Y-%m-%d").date()

            # 新しいデータの箱を作成
            new_schedule = {
                "date": p_date_obje.strftime("%Y/%m/%d"),
                "schedule": p_schedule,
                "time": "0:00",  # この時間はとりあえず初期値
            }

            # 既存データ読み込み
            with open("schedule.json") as f:
                existing_data = json.load(f)

            # 重複チェック
            if schedule_duplicate(new_schedule, existing_data):
                return jsonify({"message": "同じ予定が既にあります"})
            
            # 既存データに新しい予定を追加
            existing_data.append(new_schedule)

            # 日付の降順でソート
            existing_data.sort(key=lambda x: datetime.strptime(x["date"], "%Y/%m/%d"), reverse=False)

            # データをファイルに書き込む
            with open("schedule.json", "w") as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            return render_template("index.html")
        except Exception as e:
            return jsonify({"message": "エラーが発生しました"})


# Flaskアプリケーションの起動
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
