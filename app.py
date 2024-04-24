from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/scatterplot')
def scatterplot():
    return render_template('scatterplot.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/trendlifecycle')
def trendlifecycle():
    return render_template('trendlifecylce.html')

@app.route('/channelgrowth')
def channelgrowth():
    return render_template('channelgrowth.html')

if __name__ == '__main__':
    app.run(debug=True)