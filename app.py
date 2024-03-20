from flask import Flask, render_template
from scatterplot import generate_scatterplot
from timeline import generate_timeline

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/timeline')
def timeline():
    # Call the generate_timeline function to generate the timeline HTML
    timeline_html = generate_timeline()

    # Pass the timeline HTML to the template
    return render_template('timeline.html', timeline_html=timeline_html)

@app.route('/scatterplot')
def scatterplot():
    # Call the generate_scatterplot function to generate the scatterplot HTML
    scatterplot_html = generate_scatterplot()

    # Pass the scatterplot HTML to the template
    return render_template('scatterplot.html', scatterplot_html=scatterplot_html)

if __name__ == '__main__':
    app.run(debug=True)