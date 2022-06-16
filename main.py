from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

COFFEE_RATINGS = [' ☕️ ', ' ☕️ ☕️ ', ' ☕️ ☕️ ☕️ ', ' ☕️ ☕️ ☕️ ☕️ ', ' ☕️ ☕️ ☕️ ☕️ ☕️ ']
WIFI_RATINGS = [' ✘ ', ' 💪️ ', ' 💪️ 💪️ ', ' 💪️ 💪️ 💪️ ', ' 💪️ 💪️ 💪️ 💪️ ', ' 💪️ 💪️ 💪️ 💪️ 💪️ ']
POWER_RATINGS = [' ✘ ', ' 🔌️ ', ' 🔌️ 🔌️ ', ' 🔌️ 🔌️ 🔌️ ', ' 🔌️ 🔌️ 🔌️ 🔌️ ', ' 🔌️ 🔌️ 🔌️ 🔌️ 🔌️ ']


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)',
                           validators=[URL(message='Please enter a valid url.'), DataRequired()])
    open = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closed = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=COFFEE_RATINGS, validate_choice=True)
    wifi_rating = SelectField('Wifi Strength Rating', choices= WIFI_RATINGS, validate_choice=True)
    power = SelectField('Power Socket Availability', choices= POWER_RATINGS, validate_choice=True)
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        with open("cafe-data.csv", "a") as csv_file:
            fieldnames = ['Cafe Name', 'Location', 'Open', 'Close', 'Coffee', 'Wifi', 'Power']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({
                'Cafe Name': form.data['cafe'],
                'Location': form.data['location'],
                'Open': form.data['open'],
                'Close': form.data['closed'],
                'Coffee': form.data['coffee_rating'],
                'Wifi': form.data['wifi_rating'],
                'Power': form.data['power'],
            })
        return redirect(url_for('cafes'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
