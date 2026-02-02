import requests

BASE_URL = "http://127.0.0.1:8000/api/"

class APIClient:
    def __init__(self):
        self.session = requests.Session()

    def login(self, username, password):
        self.session.auth = (username, password)
        # Verify credentials
        try:
            r = self.session.get(BASE_URL + 'uploads/history/')
            if r.status_code == 403 or r.status_code == 401:
                return False
            return True
        except:
            return False
    
    def upload_csv(self, file_path):
        try:
            files = {'file': open(file_path, 'rb')}
            response = self.session.post(BASE_URL + 'uploads/', files=files)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as e:
            try:
                return response.json(), response.status_code
            except:
                return {"error": str(e)}, 500
        except Exception as e:
            return {"error": str(e)}, 500

    def get_summary(self, upload_id):
        try:
            response = self.session.get(BASE_URL + f'uploads/{upload_id}/summary/')
            response.raise_for_status()
            return response.json()
        except:
            return None

    def get_history(self):
        try:
            response = self.session.get(BASE_URL + 'uploads/history/')
            return response.json()
        except:
            return []

    def get_upload_detail(self, upload_id):
        try:
            response = self.session.get(BASE_URL + f'uploads/{upload_id}/')
            return response.json()
        except:
            return None
