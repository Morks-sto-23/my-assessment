import os

import numpy as np
import pandas as pd

"""
To answer the following questions, make use of datasets: 
    'scheduled_loan_repayments.csv'
    'actual_loan_repayments.csv'
These files are located in the 'data' folder. 

'scheduled_loan_repayments.csv' contains the expected monthly payments for each loan. These values are constant regardless of what is actually paid.
'actual_loan_repayments.csv' contains the actual amount paid to each loan for each month.

All loans have a loan term of 2 years with an annual interest rate of 10%. Repayments are scheduled monthly.
A type 1 default occurs on a loan when any scheduled monthly repayment is not met in full.
A type 2 default occurs on a loan when more than 15% of the expected total payments are unpaid for the year.

Note: Do not round any final answers.

"""


def calculate_df_balances(df_scheduled, df_actual):
    """
    This is a utility function that creates a merged dataframe that will be used in the following questions.
    This function will not be graded, do not make changes to it.

    Args:
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
        df_actual (DataFrame): Dataframe created from the 'actual_loan_repayments.csv' dataset

    Returns:
        DataFrame: A merged Dataframe with additional calculated columns to help with the following questions.

    """

    df_merged = pd.merge(df_actual, df_scheduled)

    def calculate_balance(group):
        r_monthly = 0.1 / 12
        group = group.sort_values("Month")
        balances = []
        interest_payments = []
        loan_start_balances = []
        for index, row in group.iterrows():
            if balances:
                interest_payment = balances[-1] * r_monthly
                balance_with_interest = balances[-1] + interest_payment
            else:
                interest_payment = row["LoanAmount"] * r_monthly
                balance_with_interest = row["LoanAmount"] + interest_payment
                loan_start_balances.append(row["LoanAmount"])

            new_balance = balance_with_interest - row["ActualRepayment"]
            interest_payments.append(interest_payment)

            new_balance = max(0, new_balance)
            balances.append(new_balance)

        loan_start_balances.extend(balances)
        loan_start_balances.pop()
        group["LoanBalanceStart"] = loan_start_balances
        group["LoanBalanceEnd"] = balances
        group["InterestPayment"] = interest_payments
        return group

    df_balances = (
        df_merged.groupby("LoanID", as_index=False)
        .apply(calculate_balance)
        .reset_index(drop=True)
    )

    df_balances["LoanBalanceEnd"] = df_balances["LoanBalanceEnd"].round(2)
    df_balances["InterestPayment"] = df_balances["InterestPayment"].round(2)
    df_balances["LoanBalanceStart"] = df_balances["LoanBalanceStart"].round(2)

    return df_balances


# Do not edit these directories
root = os.getcwd()

if "Task_2" in root:
    df_scheduled = pd.read_csv("data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("data/actual_loan_repayments.csv")
else:
    df_scheduled = pd.read_csv("Task_2/data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("Task_2/data/actual_loan_repayments.csv")

df_balances = calculate_df_balances(df_scheduled, df_actual)


def question_1(df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 1 default definition.

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The percentage of type 1 defaulted loans (ie 50.0 not 0.5)
        
        
        meaning of type 1 is when atcualPayment < scheduled 
        1 identify loans where payment was not made in full
        2 count num of defaulted loans
        3 total of unique loans ie by LoanID
        4 calc %

    """

     default_mask = df_balances["ActualRepayment"] < df_balances["ScheduledRepayment"]
     defaults = df_balances[default_mask]
 
     customers_who_defaulted = defaults["LoanID"].unique()
     num_defaults = len(customers_who_defaulted)
     total_customers = df_balances["LoanID"].nunique()
 
     default_rate = num_defaults / total_customers
     default_rate_percent = default_rate * 100

    return default_rate_percent


def question_2(df_scheduled, df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 2 default definition

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset

    Returns:
        float: The percentage of type 2 defaulted loans (ie 50.0 not 0.5)

        1 calc total scheduled repayment for each loan
        2 calc total actual repayments for each loan
        3 calc unpaid schduled payments
        4 identify loans where unpaid > 15% of sceduled
        5 get total number of loans that defaulted
        6 get total number of loans
        7 % of defaulted loans
        

    """

     df_yearly = df_scheduled
     df_yearly["YearlyScheduled"] = df_yearly["ScheduledRepayment"] * 12
 
     yearly_actual = df_balances.groupby("LoanID")["ActualRepayment"].sum().to_list()
     df_yearly["YearlyActual"] = yearly_actual
     filtr = df_yearly["YearlyActual"] <= 0.85 * df_yearly["YearlyScheduled"]
 
     num_defaults = len(df_yearly[filtr])
 
     total_customers = df_yearly["LoanID"].nunique()
 
     default_rate_percent = 100 * num_defaults / total_customers
    
    

    return default_rate_percent


def question_3(df_balances):
    """
    Calculate the anualized portfolio CPR (As a %) from the geometric mean SMM.
    SMM is calculated as: (Unscheduled Principal)/(Start of Month Loan Balance)
    SMM_mean is calculated as (∏(1+SMM))^(1/12) - 1
    CPR is calcualted as: 1 - (1- SMM_mean)^12

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The anualized CPR of the loan portfolio as a percent.

        1 calc SMM (Unscheduled Principal)/(Start of Month Loan Balance)
        2 remove NAN values where /0 
        3 calc geometric mean (1 + smm) over 12 months
        4 calc cpr
        5 %

    """

     df_smm = pd.DataFrame()
     df_smm["UnscheduledPrincipal"] = df_balances.groupby(df_balances["Month"])[
         "UnscheduledPrincipal"
     ].sum()
     df_smm["LoanPortfolioBalance"] = df_balances.groupby(df_balances["Month"])[
         "LoanBalanceStart"
     ].sum()
     df_smm["SMM"] = (df_smm["UnscheduledPrincipal"]) / df_smm["LoanPortfolioBalance"]
     df_smm.reset_index(inplace=True)
 
     mean_smm = ((1 + df_smm["SMM"]).prod()) ** (1 / 12) - 1
     cpr = 1 - (1 - mean_smm) ** 12
     cpr_percent = 100 * cpr
    
    

    return cpr_percent


def question_4(df_balances,type_2_default_rate):
    """
    Calculate the predicted total loss for the second year in the loan term.
    Use the equation: probability_of_default * total_loan_balance * (1 - recovery_rate).
    The probability_of_default value must be taken from either your question_1 or question_2 answer.
    Decide between the two answers based on which default definition you believe to be the more useful metric.
    Assume a recovery rate of 80%

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The predicted total loss for the second year in the loan term.
        1 define recovery rate
        2 convert type 2 % to probability
        3 get total loan balance at start of y2
        4 predict loss 
        

    """
    
     probability_of_default = question_2(df_scheduled, df_balances) / 100
 
     total_loan_balance_list = df_balances.groupby(df_balances["Month"])[
         "LoanBalanceEnd"
     ].sum()
     total_loan_balance_final = total_loan_balance_list[12]
 
     total_loss = probability_of_default * total_loan_balance_final * (1 - 0.8)
    
    return total_loss
