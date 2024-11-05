account_balance = 1500

try:
    user_withdrawl = int(input("Enter the amount you want to withdraw: "))
    if user_withdrawl < account_balance:
        new_balance = account_balance - user_withdrawl
        print("You have successfully withdrawn: ", user_withdrawl)
        print("Your new balance is: ", new_balance)
    else:
        print("Insufficient funds")
except ValueError:
    print("Please enter a valid number")
    print("Your account balance is: ", account_balance)