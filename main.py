import os
import base64
import peewee

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor, db

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        donor_name = request.form['name']
        donation_val = int(request.form['donation'])
        with db.transaction():
            try:
                new_donor = Donor.create(name=donor_name)
                new_donor.save()
            except peewee.IntegrityError:
                new_donor = Donor.get(Donor.name == donor_name)
            donation = Donation.create(donor=new_donor,
                                value=donation_val)
            donation.save()
        return redirect(url_for('all'))
    return render_template('create.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
