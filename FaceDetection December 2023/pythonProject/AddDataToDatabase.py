import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,{
   'databaseURL':"https://imgid-3de22-default-rtdb.firebaseio.com/"
})
ref = db.reference('IDP')
data = {
    "112255":
        {
            "name": "Elon Musk",
            "phone": "0799312323",
            "stat": "Active",
            "Number": "3",
        },
    "112277":
        {
            "name": "feras khirfan",
            "phone": "0790696775",
            "stat": "Active",
            "Number": "4",
        },
    "112266":
        {
            "name": "mohammad elewat",
            "phone": "0790556775",
            "stat": "Active",
            "Number": "5",
        },
    "112299": {
        "name": "qutaibah subeh",
        "phone": "076485213",
        "stat": "Active",
        "Number": "7",

    }
}

for key, value in data.items():
    ref.child(key).set(value)
