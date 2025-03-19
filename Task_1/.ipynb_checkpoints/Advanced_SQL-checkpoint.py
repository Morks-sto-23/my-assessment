"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)

NOTE:
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""


def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    qry = """select c.CustomerClass , avg(cl.Income) as AverageIncome 
             from customers cl join credit c on cl.CustomerID = c.CustomerID 
             group by c.CustomerClass """

    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

    qry = """select c.Region, count(l.CustomerID) as RejectedApplications 
             from customers c join loans l on c.CustomerID = l.CustomerID where l.ApprovalStatus = 'Rejected' 
             group by c.Region order by RejectedApplications desc """

    return qry


def question_3():
    """
    Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    qry = """Create table financing (
             CustomerID int primary key,
             Income decimal(10,2),
             LoanAmount decimal(10,2),
             LoanTerm int,
             IntrestRate decimal(5,2),
             ApprovalStatus varchar(20),
             CreditScore int );"""

    return qry


# Question 4 and 5 are linked


def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time.
    Null values to be filled with 0.

    Hint: there should be 12x CustomerID = 1.

  
    """

    qry = """   Create table timeline(
                CustomerID int,
                MonthName varchar(20),
                NumberOfRepayments int default 0, 
                AmountTotal decimal(10,2) default 0,
                Primary Key (CustomerID,MonthName));

                
              insert into timeline(CustomerID, MonthName, NumberOfRepayments, AmountTotal)
              select c.CustomerID, m.MonthName,
              COALESCE(count(r.RepaymentID),0) as NumberOfRepayments,
              COALESCE(sum(r.Amount),0 )as AmountTotal 
              from customers c 
              cross join months m 
              left join repayments r
              on c.CustomerID = r.CustomerID
              and extract(MONTH from r.RepaymentDate) = m.MonthID
              and cast(r.RepaymentDate as time) between '06:00:00' and '18:00:00'
              group by c.CustomerID, m.MonthName
              order by c.CustomerID, m.MonthName;"""

    return qry


def question_5():
    """
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """

    qry = """select CustomerID,
            SUM(CASE WHEN MonthName = 'January' THEN NumberOfRepayments ELSE 0 END) AS JanuaryRepayments,
            SUM(CASE WHEN MonthName = 'January' THEN AmountTotal ELSE 0 END) AS JanuaryTotal,
            SUM(CASE WHEN MonthName = 'February' THEN NumberOfRepayments ELSE 0 END) AS FebruaryRepayments,
            SUM(CASE WHEN MonthName = 'February' THEN AmountTotal ELSE 0 END) AS FebruaryTotal,
            SUM(CASE WHEN MonthName = 'March' THEN NumberOfRepayments ELSE 0 END) AS MarchRepayments,
            SUM(CASE WHEN MonthName = 'March' THEN AmountTotal ELSE 0 END) AS MarchTotal,
            SUM(CASE WHEN MonthName = 'April' THEN NumberOfRepayments ELSE 0 END) AS AprilRepayments,
            SUM(CASE WHEN MonthName = 'April' THEN AmountTotal ELSE 0 END) AS AprilTotal,
            SUM(CASE WHEN MonthName = 'May' THEN NumberOfRepayments ELSE 0 END) AS MayRepayments,
            SUM(CASE WHEN MonthName = 'May' THEN AmountTotal ELSE 0 END) AS MayTotal,
            SUM(CASE WHEN MonthName = 'June' THEN NumberOfRepayments ELSE 0 END) AS JuneRepayments,
            SUM(CASE WHEN MonthName = 'June' THEN AmountTotal ELSE 0 END) AS JuneTotal,
            SUM(CASE WHEN MonthName = 'July' THEN NumberOfRepayments ELSE 0 END) AS JulyRepayments,
            SUM(CASE WHEN MonthName = 'July' THEN AmountTotal ELSE 0 END) AS JulyTotal,
            SUM(CASE WHEN MonthName = 'August' THEN NumberOfRepayments ELSE 0 END) AS AugustRepayments,
            SUM(CASE WHEN MonthName = 'August' THEN AmountTotal ELSE 0 END) AS AugustTotal,
            SUM(CASE WHEN MonthName = 'September' THEN NumberOfRepayments ELSE 0 END) AS SeptemberRepayments,
            SUM(CASE WHEN MonthName = 'September' THEN AmountTotal ELSE 0 END) AS SeptemberTotal,
            SUM(CASE WHEN MonthName = 'October' THEN NumberOfRepayments ELSE 0 END) AS OctoberRepayments,
            SUM(CASE WHEN MonthName = 'October' THEN AmountTotal ELSE 0 END) AS OctoberTotal,
            SUM(CASE WHEN MonthName = 'November' THEN NumberOfRepayments ELSE 0 END) AS NovemberRepayments,
            SUM(CASE WHEN MonthName = 'November' THEN AmountTotal ELSE 0 END) AS NovemberTotal,
            SUM(CASE WHEN MonthName = 'December' THEN NumberOfRepayments ELSE 0 END) AS DecemberRepayments,
            SUM(CASE WHEN MonthName = 'December' THEN AmountTotal ELSE 0 END) AS DecemberTotal
            from timeline
            group by CustomerID
            order by CustomerID;"""

    return qry


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these question.


def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """

    qry = """ create table corrected_customers(
              CustomerID int primary key, 
              Age int, 
              CorrectedAge int,
              Gender varchar(10));

              insert into corrected_customers (CustomerID, Age, CorrectedAge, Gender)
              select distinct on (CustomerID) CustomerID, Age, coalesce(lag(Age,2) over (partition by Gender order by CustomerID),
              FIRST_VALUE(Age) over (partition by Gender order by CustomerID)) as CorrectedAge,Gender
              from customers;
              select * from corrected_customers;
     """

    return qry


def question_7():
    """
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`

    1 add age cat
    2 update age cat based on updatedAge
    3 add rank col
    4 create temp tbl to calculate repayments
    5 update rank col 
    6 retun res 
    """

    qry = """ alter table corrected_customers 
              add column AgeCategory varchar(20);


              update corrected_Customers
              set AgeCategory = case when CorrectedAge <20 then 'teen' 
                                     when CorrectedAge between 20 and 29 then 'Young Adult'
                                     when CorrectedAge between 30 and 59 then 'Adult'
                                     else 'Pensioner'
                                     end ;
                                     
              alter table corrected_customers
              add column Rank int ;

              with RepaymentTotals as ( select c.CustomerID, c.Age, c.CorrectedAge, c.Gender,c.AgeCategory,
              coalesce (count(r.RepaymentID),0) as TotalRepayments 
              from corrected_customers c 
              left join repayments r on c.CustomerID = r.CustomerID
              group by c.CustomerID, c.Age, c.Gender, c.CorrectedAge, c.Gender, c.AgeCategory),RankedCustomers 
              as (select CustomerID, Age, CorrectedAge, Gender, AgeCategory, TotalRepayments,
              Dense_Rank() over (partition by AgeCategory order by TotalRepayments desc ) as Rank
              from RepaymentTotals)

              update corrected_customers 
              set Rank = RankedCustomers.Rank 
              from RankedCustomers where corrected_customers.CustomerID = RankedCustomers.CustomerID;

              select CustomerID,Age,CorrectedAge, Gender,AgeCategory, Rank from corrected_customers;
              
              
              
              
              """

    return qry
