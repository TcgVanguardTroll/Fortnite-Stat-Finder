import requests
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='jjgrant', api_key='A9MQ3mU458oWAcL3k6ip')
from flask import Flask, render_template, request 

URL = 'https://api.fortnitetracker.com/v1/profile/{}/{}'
headers = {'TRN-Api-Key' : 'c01d512b-474d-463f-966e-47cab404a5b7'}

# res = requests.get(URL, headers=headers)
# result = res.json()['lifeTimeStats']

app = Flask(__name__)

# print(result)


@app.route('/', methods=['GET', 'POST' ])

def index():
    player_one = None
    player_stats = {}

    if request.method == 'POST':
        try:
            player_one = request.form.get('epicUsername')
            console = request.form['Item_1']
            if player_one:
                pass
            else:
                player_one = request.form.get('playerName')
        except KeyError:
            return False
            
        player_one_result = requests.get(URL.format(console,player_one), headers=headers).json()['lifeTimeStats']
        player_stats = populate_player_data(player_one_result)
        visual = plot(player_one_result)

    return render_template('index.html', player_one=player_one,
        player_stats=player_stats,visual=plot)
def populate_player_data(data):

    diction = {}

    for x in data:
    
        if x['key'] == 'K/d':
            diction['k/d'] = x['value']
        if x['key'] == 'Kills':
            diction['kills'] = x['value']
        if x['key'] == 'Matches Played':
            diction['matches'] = x['value']
    return diction
    return plot

def plot(data):
    labels = ['Kills Per Minute','Win Percentage']
    values = []
    for x in data:
        if x['key'] == 'Kills Per Minute':
            values.append(x['value'])
        if x['key'] == 'Win%':
            values.append(x['value'])
        if x['key'] == 'Matches Played':
            values.append(x['value'])
    trace = go.Pie(labels=labels, values=values)
    return py.plot([trace], filename='basic_pie_chart')
    
if __name__ == '__main__':
    app.run(debug = True)