from app import db

class AirVisualDeviceMeasurement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    co2 = db.Column(db.Float)
    pm25_conc = db.Column(db.Float)
    pm25_aqius = db.Column(db.Float)
    pm25_aqicn = db.Column(db.Float)
    pm10_conc = db.Column(db.Float)
    pm10_aqius = db.Column(db.Float)
    pm10_aqicn = db.Column(db.Float)
    pm1_conc = db.Column(db.Float)
    pm1_aqius = db.Column(db.Float)
    pm1_aqicn = db.Column(db.Float)
    pr = db.Column(db.Float)
    hm = db.Column(db.Float)
    tp = db.Column(db.Float)
    aqius = db.Column(db.Float)
    aqicn = db.Column(db.Float)
    mainus = db.Column(db.String)
    maincn = db.Column(db.String)
    ts = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "co_2": self.co2,
            "mainus": self.mainus,
            "maincn": self.maincn,
            "ts": self.ts,
            "pm_25": {
                "conc": self.pm25_conc,
                "aqius": self.pm25_aqius,
                "aqicn": self.pm25_aqicn
            },
            "pm_10" :{
                "conc": self.pm10_conc,
                "aqius": self.pm10_aqius,
                "aqicn": self.pm10_aqicn,
            },
            "pm_1": {
                "conc": self.pm1_conc,
                "aqius": self.pm1_aqius,
                "aqicn": self.pm1_aqicn,
            },
            "pr": self.pr,
            "hm": self.hm,
            "tp": self.tp,
            "aqius": self.aqius,
            "aqicn": self.aqicn,
            "created_at": self.created_at.isoformat()
        }
