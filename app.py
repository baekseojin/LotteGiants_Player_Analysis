from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

app = Flask(__name__)

def scrape_player_data(player_name):
    url = 'http://www.statiz.co.kr/player.php?name=전준우'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find_all("table")[2]

    df = pd.DataFrame(index=range(30), columns=["연도", "팀", "나이", "포지션", "게임수", "타석", "타수", "득점", "안타", "2루타", "3루타", "홈런", "루타", "타점", "도루", "도루실패", "볼넷", "사구", "고의사구", "삼진", "병살", "희생타", "희생플라이", "타율", "출루율", "장타율", "OPS", "wOBA", "WRC", "WAR", "WPA"])

    l = 0
    temp2 = temp.find_all("tr")[0]
    for j in range(0, 4):
        temp2 = temp.find_all("tr")[j]
        if len(temp2.find_all("td")) == 31:
            for i in range(31):
                temp3 = temp2.find_all("td")[i]
                df.iloc[l, i] = temp3.get_text()
            l += 1

    return df

def generate_player_graph(player_name):
    player_data = scrape_player_data(player_name)

    if player_data.empty:
        return None  # 선수 데이터가 없을 경우 None 반환

    # 선수별 성적 시각화
    fig = px.bar(player_data, x='연도', y=['WAR', '게임수', '홈런', '타율'],
                 title=f'Statistics for {player_name} in 2023')  # 연도를 항상 2023년으로 고정
    return fig

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_name = request.form['player_name']
        fig = generate_player_graph(player_name)

        if fig:
            graph_html = fig.to_html(full_html=False)
        else:
            graph_html = "<p>선수 정보를 찾을 수 없습니다.</p>"

        return render_template('index.html', graph_html=graph_html, player_name=player_name)

    return render_template('index.html', graph_html='', player_name='')

if __name__ == '__main__':
    app.run(debug=True)
