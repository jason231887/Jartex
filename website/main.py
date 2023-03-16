from flask import Flask, render_template
import pandas 

url = f'https://docs.google.com/spreadsheets/d/1UonkKjgG95Hkz-zPedfyPu9PDjd_YQHmEI9e3mf-NRM/export?format=csv'

app = Flask(__name__)

headings = ('Name', 'Item', 'Date')

#Remove first row, consisting of headings
df = pandas.read_csv(url, usecols=[0,1,2])
data = list(df.itertuples(index=False, name=None))

@app.route("/")
def table():
    return render_template("index.html", headings=headings, data=data)

if __name__ == '__main__':
    app.run()
