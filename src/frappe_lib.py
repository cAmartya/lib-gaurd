import requests

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
        if "page" not in query.keys():
            query["page"] = page
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
        
    def get_img_from_isbn(self, isbn: str) -> str:
        if isbn == "https://avatars.githubusercontent.com/u/80196675?v=4":
            return
        return f"{self.open_lib_url}/{isbn}-M.jpg"

frappe_client=FrappeLib()

        



