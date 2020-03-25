from . import db

#this is the model for the rpi table in the db -jared
class Rpi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pin_code = db.Column(db.String(150))

    def __repr__(self):
        return self.id

def create_rpi(rpi):
    db.session.add(rpi)
    db.session.commit()

#Update pi's pin code - Adrian
def update_pi(pi, pin_code):
    pi.pin_code = pin_code
    db.session.commit()

#Queries pi - Adrian
def query_rpi():
    try:
        print(db.session.query(Rpi.id).count())
        return Rpi.query.filter_by(id=1).first()
    except:
        raise

    
