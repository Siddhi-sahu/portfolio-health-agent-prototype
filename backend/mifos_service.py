import requests

BASE_URL = "https://demo.mifos.io/fineract-provider/api/v1"

HEADERS = {
    "Authorization": "Basic bWlmb3M6cGFzc3dvcmQ=",
    "fineract-platform-tenantid": "default",
    "Content-Type": "application/json"
}


from mock_data import mock_loans


def fetch_loans():

    url = f"{BASE_URL}/loans?limit=10&offset=0"
    # url = f"{BASE_URL}/loans?limit=30&offset=20"

    try:

        response = requests.get(
            url,
            headers=HEADERS,
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:

            print("MIFOS FAILED — USING MOCK DATA")

            return {
                "pageItems": mock_loans
            }

        return response.json()

    except Exception as e:

        print("FETCH ERROR:", str(e))

        print("USING MOCK DATA")

        return {
            "pageItems": mock_loans
        }


def transform_loan(mifos_loan):

    delinquent_data = mifos_loan.get("delinquent", {})

    days_late = delinquent_data.get("pastDueDays", 0)

    delinquent_amount = delinquent_data.get(
        "delinquentAmount",
        0
    )

    loan_amount = mifos_loan.get("principal", 0)

    in_arrears = mifos_loan.get("inArrears", False)

    is_npa = mifos_loan.get("isNPA", False)

    loan_status = mifos_loan.get(
        "status",
        {}
    ).get(
        "value",
        "UNKNOWN"
    )

    risk_flags = []

    if days_late > 30:
        risk_flags.append("HIGH_DPD")

    if in_arrears:
        risk_flags.append("IN_ARREARS")

    if is_npa:
        risk_flags.append("NPA_ACCOUNT")

    if loan_amount > 500000:
        risk_flags.append("HIGH_EXPOSURE")

    return {
        "clientName": mifos_loan.get(
            "clientName",
            "Unknown"
        ),

        "daysLate": days_late,

        "loanAmount": loan_amount,

        "missedPayments": max(
            0,
            days_late // 30
        ),

        "inArrears": in_arrears,

        "isNPA": is_npa,

        "delinquentAmount": delinquent_amount,

        "riskFlags": risk_flags,

        "loanStatus": loan_status
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