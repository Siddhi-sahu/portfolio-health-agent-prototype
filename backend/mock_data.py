mock_loans = [
    {
        "clientName": "Ravi",

        "principal": 70000,

        "inArrears": True,

        "isNPA": False,

        "status": {
            "value": "Active"
        },

        "delinquent": {
            "pastDueDays": 45,
            "delinquentAmount": 15000
        }
    },

    {
        "clientName": "Anita",

        "principal": 25000,

        "inArrears": False,

        "isNPA": False,

        "status": {
            "value": "Active"
        },

        "delinquent": {
            "pastDueDays": 5,
            "delinquentAmount": 1000
        }
    },

    {
        "clientName": "Mohan",

        "principal": 600000,

        "inArrears": True,

        "isNPA": True,

        "status": {
            "value": "Active"
        },

        "delinquent": {
            "pastDueDays": 90,
            "delinquentAmount": 85000
        }
    }
]