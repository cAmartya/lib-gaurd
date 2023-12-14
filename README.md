# LibGaurd - Library Management Application

**LibGaurd** helps to manage your library with ease.

---

### Features
- Search books by title, author, isbn, publisher
- Add / Edit / Delete books
- Import books from Frappe API
- Add / Edit / Delete members
- View books transactions
- Issue / Return books

### Live Demo
Check out the live demo here - 

*Test Credentials*
 - *Username*: `test`
 - *Password*: `test`

### Installation
-   #### Using Docker
    - Clone the repo
        ```bash
      git clone https://github.com/cAmartya/lib-gaurd.git
      ```
    
    - Run the following command
        ```bash
        sudo docker compose up
        ```
    - Visit http://localhost:8000

-   #### Using Python
    - Clone the repo
        ```bash
      git clone https://github.com/cAmartya/lib-gaurd.git
      ```
    
    - Copy the contents of `.env.example` to `.env`.
    - Install the python dependencies
        ```bash
        pip install -r requirements.txt
        ```
    - Run the following command
        ```bash
        python src/main.py
        ```
    - Visit http://localhost:8000

### Tech Stack
- Python
- Flask
- Flask SQLAlchemy
- Bootstrap

### Screenshots
- **Login To LibGaurd**
![Login To LibGaurd](screenshots/auth.png)

- **Search & List Books**
![Search & List Books](screenshots/books.png)

- **Add Books**
![Add Books](screenshots/add_book.png)

- **Import Books**
![Import Books](screenshots/import_book.png)

- **Show Book Details**
![Show Book Details](screenshots/view_book.png)

- **Issue Book**
![Issue Book](screenshots/issue.png)

- **Members List**
![Members List](screenshots/members.png)

- **Add New Member**
![Add New Member](screenshots/add_member.png)

- **Transaction Records**
![Transaction Records](screenshots/transactions.png)

### Disclaimer
This project is a part of the [Frappe Dev Hiring Test](https://frappe.io/dev-hiring-test).