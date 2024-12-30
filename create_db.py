from ext import db, app
from models import User, News, University



universities= [
    {
        "name": "თსუ",
        "rank": 1,
        "location": "თბილისი",
        "founded": 1918,
        "programs_offered": "Various",
        "tuition_fee_min": 1500.00,
        "tuition_fee_max": 5000.00,
        "website": "https://www.tsu.ge/",
        "logo_url": "{{ url_for('static', filename='tbc-logo.png') }}"
    },
    {
        "name": "გაუ",
        "rank": 2,
        "location": "თბილისი",
        "founded": 2001,
        "programs_offered": "Various",
        "tuition_fee_min": 1200.00,
        "tuition_fee_max": 4500.00,
        "website": "https://gau.edu.ge/ka",
        "logo_url": "https://example.com/gtu_logo.png"
    },
    {
        "name": "ისუ",
        "rank": 3,
        "location": "თბილისი",
        "founded": 1995,
        "programs_offered": "Various",
        "tuition_fee_min": 2000.00,
        "tuition_fee_max": 6000.00,
        "website": "www.isu.edu.ge",
        "logo_url": "https://example.com/isu_logo.png"
    },
    {
        "name": "თავისუფალი უნივერსიტეტი",
        "rank": 4,
        "location": "თბილისი",
        "founded": 2004,
        "programs_offered": "Various",
        "tuition_fee_min": 2500.00,
        "tuition_fee_max": 7000.00,
        "website": "www.freeuni.edu.ge",
        "logo_url": "https://example.com/freeuni_logo.png"
    },
    {
        "name": "თბილისის კავკასიის უნივერსიტეტი",
        "rank": 5,
        "location": "თბილისი",
        "founded": 2004,
        "programs_offered": "Various",
        "tuition_fee_min": 2300.00,
        "tuition_fee_max": 6500.00,
        "website": "www.cu.edu.ge",
        "logo_url": "https://example.com/cu_logo.png"
    },
    {
        "name": "Batumi Shota Rustaveli State University",
        "rank": 6,
        "location": "Batumi",
        "founded": 1923,
        "programs_offered": "Various",
        "tuition_fee_min": 1000.00,
        "tuition_fee_max": 3000.00,
        "website": "www.bsu.edu.ge",
        "logo_url": "https://example.com/bsu_logo.png"
    }
]

with app.app_context():

    db.create_all()


    universities = [University(**data) for data in universities]
    db.session.add_all(universities)

    db.session.commit()
