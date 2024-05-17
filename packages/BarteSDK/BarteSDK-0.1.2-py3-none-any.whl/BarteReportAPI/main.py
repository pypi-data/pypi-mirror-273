import requests

class BarteReportAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api2.barte.com/function/report-sellers'

    def send_report(self, query_file, recipient_email, id_seller, report_name, days_ago):
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'query_file': query_file,
            'recipient_email': recipient_email,
            'id_seller': id_seller,
            'report_name': report_name,
            'days_ago': days_ago
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.json()
