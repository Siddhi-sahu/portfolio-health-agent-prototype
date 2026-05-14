import requests

BASE_URL = "https://demo.mifos.io/fineract-provider/api/v1"

HEADERS = {
    "Authorization": "Basic bWlmb3M6cGFzc3dvcmQ=",
    "fineract-platform-tenantid": "default",
    "Content-Type": "application/json"
}


def fetch_loans():
    url = f"{BASE_URL}/loans"

    response = requests.get(url, headers=HEADERS)

    print("STATUS:", response.status_code)

    return response.json()


def transform_loan(mifos_loan):
    delinquent_data = mifos_loan.get("delinquent") or {}

    return {
        "clientName": mifos_loan.get("clientName", "Unknown"),
        "daysLate": delinquent_data.get("pastDueDays", 0),
        "loanAmount": mifos_loan.get("principal", 0),
        "missedPayments": 0
    }
    
def get_transformed_loans():
    data = fetch_loans()

    loans = data.get("pageItems", [])

    transformed_loans = []

    for loan in loans:
        transformed = transform_loan(loan)
        transformed_loans.append(transformed)

    return transformed_loans
#--
# data = fetch_loans()

# print(type(data))
# print(data)
# print(data.keys())
# print(data["pageItems"][0])
# loan = data["pageItems"][20]

# print("CLIENT:", loan.get("clientName"))
# print("PRINCIPAL:", loan.get("principal"))
# print("IN ARREARS:", loan.get("inArrears"))
# print("DELINQUENT:", loan.get("delinquent"))

# data = fetch_loans()

# loan = data["pageItems"][20]

# transformed = transform_loan(loan)

# print(transformed)