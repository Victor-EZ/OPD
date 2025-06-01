from flask import Flask, render_template, request
import math

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("lr3.html")

@app.route('/', methods=['post', 'get'])
def form():
    if request.method == 'POST':
        value = float(request.form.get('value'))
        precision = int(request.form.get('precision'))

        if request.form['units'] == "degrees":
            value *= math.pi / 180

        sin_ = round(math.sin(value), precision)
        cos_ = round(math.cos(value), precision)
        tg_ = "Не вычисляется"
        ctg_ = tg_

        if cos_:
            tg_ = round(sin_ / cos_, precision)

        if sin_:
            ctg_ = round(cos_ / sin_, precision)

        return render_template('lr3.html', sin=sin_, cos=cos_, tg=tg_, ctg=ctg_)

    return render_template('lr3.html')


if __name__ == '__main__':
    app.run()