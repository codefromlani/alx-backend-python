# Python MySQL Generator – seed.py

## Objective

Create a Python script that streams rows from a MySQL database one by one using a generator.

---

## ⚙️ What It Does

The script `seed.py`:

- Sets up a MySQL database **ALX_prodev**  
- Creates a `user_data` table with the following fields:  
  - `user_id` (Primary Key, UUID, Indexed)  
  - `name` (VARCHAR, NOT NULL)  
  - `email` (VARCHAR, NOT NULL)  
  - `age` (DECIMAL, NOT NULL)  
- Populates the table from `user_data.csv`    

---

## 🔧 Functions

- `connect_db()` – Connects to the MySQL server  
- `create_database(connection)` – Creates the `ALX_prodev` database if it doesn’t exist  
- `connect_to_prodev()` – Connects to the `ALX_prodev` database  
- `create_table(connection)` – Creates the `user_data` table if not present  
- `insert_data(connection, data)` – Inserts data from a CSV file into the database   

---

## 📦 Requirements

- Python 3.x  
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)  
- [python-dotenv](https://pypi.org/project/python-dotenv/)  

- A `.env` file with the following variables:

```env
DB_HOST=localhost
DB_USER=<your_mysql_user>
DB_PASSWORD=<your_mysql_password>
DB_NAME=ALX_prodev
