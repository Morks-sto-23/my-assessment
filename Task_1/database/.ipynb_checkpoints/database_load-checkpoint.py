import duckdb
import os
import subprocess

# Delete the existing loan.db if it exists
database_path = os.path.join(os.path.dirname(__file__), 'loan.db')
if os.path.exists(database_path):
    os.remove(database_path)
cursor = duckdb.connect(database_path)


 
def data_file_path(filename):
    "function to get correct path to data files"
    data_dir = os.path.join(os.path.dirname(__file__),'data')
    return os.path.join(data_dir, filename)




loan_qry = """CREATE TABLE loans AS SELECT * FROM read_csv(?, header=True, columns = {
               'CustomerID':'INTEGER',
               'LoanAmount':'INTEGER',
               'LoanTerm':'INTEGER',
               'InterestRate':'FLOAT',
               'ApprovalStatus':'STRING'
               })"""

cursor.execute(loan_qry, [data_file_path('loan_dataset.csv')])





customer_qry = """CREATE TABLE customers AS SELECT * FROM read_csv(?, header=True, columns = {
               'CustomerID':'INTEGER',
               'Name':'STRING',
               'Surname':'STRING',
               'Age':'INTEGER',
               'Gender':'STRING',
               'Income':'INTEGER',
               'Region':'STRING'
               })"""

cursor.execute(customer_qry, [data_file_path('customer_data.csv')])




credit_qry = """CREATE TABLE credit AS SELECT * FROM read_csv(?, header=True, columns = {
               'CustomerID':'INTEGER',
               'CreditScore':'INTEGER',
               'CustomerClass':'STRING'
               })"""

cursor.execute(credit_qry, [data_file_path('credit_data.csv')])




repayment_qry = """CREATE TABLE repayments AS SELECT * FROM read_csv(?, header=True, columns = {
               'RepaymentID':'INTEGER',
               'RepaymentDate':'TIMESTAMP',
               'Amount':'INTEGER',
               'CustomerID':'INTEGER',
               'TimeZone' : 'String'
               })"""

cursor.execute(repayment_qry, [data_file_path('Loan_Repayments.csv')])




months_qry = """CREATE TABLE months AS SELECT * FROM read_csv(?, header=True, columns = {
               'MonthID':'INTEGER',
               'MonthName':'STRING',
               })"""

cursor.execute(months_qry, [data_file_path('Months.csv')])




cursor.close()





