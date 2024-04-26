from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trendComparison')
def trendComparison():
    return render_template('trendComparison.html')

@app.route('/engagementRecap')
def engagementRecap():
    return render_template('engagementRecap.html')

@app.route('/globalView')
def globalView():
    return render_template('globalView.html')

@app.route('/channelInsight')
def channelInsight():
    return render_template('channelInsight.html')


if __name__ == '__main__':
    app.run(debug=True)