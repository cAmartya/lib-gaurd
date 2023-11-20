import requests, os
# from app import app

class FrappeLib:
    def __init__(self) -> None:
        self.__client = None
        self.frappe_url="https://frappe.io/api/method/frappe-library"
        self.open_lib_url="https://covers.openlibrary.org/b/isbn"
    # def get_client(self):
    #     if self.__client is None:
    #         pass
    #     pass

    def get_books(self, query:dict=dict(), page:int=1)-> []:
        # if "page" not in query.keys():
        #     query["page"] = page
        print(query)
        try:
            res = requests.get(self.frappe_url, params=query)
            if res.status_code == 200:
                res = res.json()
                return res["message"]
            return []
        except Exception as e:
            print("can't get books from frappe", e)
            return[]
        
    def get_img_from_isbn(self, directory:str, isbn: str) -> None:
        res = requests.get(f"{self.open_lib_url}/{isbn}-M.jpg")
        if res.status_code == 200:
            # with open(os.path.join(app.config["UPLOAD_FOLDER"], isbn), 'wb') as f:
            #     f.write(res.content)
            with open(os.path.join(directory, isbn), 'wb') as f:
                f.write(res.content)
        # else:
        #     with open(os.path.join(directory, isbn), 'wb') as f:
        #         f.write()

frappe_client=FrappeLib()

        



