from User import *
from BankAccount import * 
from Transaction import *
 
class GpayController:
    def __init__(self):
        self.dataStore = {}
 
    def handleSignup(self):
        while True:
            mobileNumber = input("Enter your mobile number: ")
            if len(mobileNumber) != 10:
                print("Enter valid mobile number")
            else:
                break
        if mobileNumber in self.dataStore:
            print("Account existed with this mobile number, kindly pleas login")
            return
        while True:
            otp = input("Enter the 4-digit OTP: ")
            if len(otp) != 4:
                print("Please enter 4-digit OTP")
            else:
                break
        fullName = input("Enter your fullName: ")
 
        while True:
            while True:
                securityPin1 = input("Select 4-digit pin: ")
                if len(securityPin1) != 4:
                    print("Please select 4 -digit PIN only")
                else:
                    break
            securityPin2 = input("Re-Enter the 4-digit security Pin: ")
            if securityPin1 != securityPin2:
                print("Pin didn't matched, kindly please try again")
            else:
                print("Pin set successfully")
                break
 
        newUser = User()
        newUser.fullName = fullName 
        newUser.pin = securityPin1 
        newUser.mobileNumber = mobileNumber
        self.dataStore[mobileNumber] = newUser 
        print("Data inserted into database successfully")
 
 
    def handleLogin(self):
        mobileNumber = input("Enter your registered mobile number: ")
        if mobileNumber not in self.dataStore:
            print("User haven't registered yet on G-Pay, kindly please register first before login")
            return 
        user = self.dataStore[mobileNumber]
        availableAttempts = 3 
        enteredCorrectPin = False 
 
        while availableAttempts > 0:
            pin = input("Enter your 4-digit security pin: ")
            if user.pin != pin:
                if availableAttempts - 1 == 0:
                    print("Your account temporarily blocked for next 24 hours")
                else:
                    print("Wrong pin, you have", (availableAttempts - 1), " attempts left")
            else:
                enteredCorrectPin = True
                break
            availableAttempts -= 1
 
        if enteredCorrectPin == True:
            self.handleLoginMenu(user)
 
    def handleLoginMenu(self, user):
        while True:
            print("\n\n\n***********************************")
            print("1 - Add Bank account")
            print("2 - Check Balance")
            print("3 - Send Money to Others")
            print("4 - Self Transfer")
            print("5 - Transaction history")
            print("6 - Deposit from CDM")
            print("7 - Logout")
            print("***********************************")
            choice = int(input("Choose your option: "))
 
            if choice == 1:
                self.handleAddBankAccounts(user)
            elif choice == 2:
                self.handleCheckBalance(user)
            elif choice == 3:
                self.handleSendMoneyToOthers(user)
            elif choice == 4:
                self.handleSelfTransfer(user)
            elif choice == 5:
                self.handlePrintPreviousTransactions(user)
            elif choice == 6:
                self.handleDepositInCDM(user)
            elif choice == 7:
                print("Logging out")
                return
            else:
                print("Select appropriate option")
 
 
    def handleAddBankAccounts(self, user):
        bankName = input("Enter Bank name: ")
        for bank in user.linkedBankAccounts:
            if bank.bankName == bankName:
                print("Already bank was added earlier")
                return 
 
        newBank = BankAccount()
        newBank.bankName = bankName 
        if len(user.linkedBankAccounts) == 0:
            user.defaultBankAccount = newBank 
        else:
            option = input("Do you want to set this bank as default account ? (y or n)")
            if option == 'y':
                user.defaultBankAccount = newBank
        user.linkedBankAccounts.append(newBank)
        print("Added ", bankName, " successfully")
        print("Default bank name is: ", user.defaultBankAccount.bankName)
 
    def handleCheckBalance(self, user):
        if len(user.linkedBankAccounts) == 0:
            print("No Bank accounts linked")
            return 
 
        position = 1 
        for bank in user.linkedBankAccounts:
            print(position, " - ", bank.bankName)
            position += 1 
        option = int(input("Choose the bank number"))
        option -= 1 
        bankAccount = user.linkedBankAccounts[option]
        print("Balance in: ", bankAccount.bankName, " is: ", bankAccount.balance)
 
    def handleDepositInCDM(self, user):
        if len(user.linkedBankAccounts) == 0:
            print("No Bank accounts linked")
            return 
        amountToBeDeposited = int(input("Enter the amount to be deposited: "))
        position = 1 
        for bank in user.linkedBankAccounts:
            print(position, " - ", bank.bankName)
            position += 1 
        option = int(input("Choose the bank number"))
        option -= 1 
        bankAccount = user.linkedBankAccounts[option]
        bankAccount.balance += amountToBeDeposited
        choice = input("Do you want to display the current balance on screen ? (y or n)")[0]
        if choice == 'y':
            print("Your total balance in: ", bankAccount.bankName, " is: ", bankAccount.balance)
        print("Deposited successfully")
 
 
    def handleSendMoneyToOthers(self, user):
        if len(user.linkedBankAccounts) == 0:
            print("No Bank accounts linked")
            return 
        receiverNumber = input("Enter receiver mobile number: ")
        if receiverNumber not in self.dataStore:
            print("Receiver didn't registered on G-Pay")
            return
        receiverUserObject = self.dataStore[receiverNumber]
        print("Receiver name is: ", receiverUserObject.fullName)
        choice = input("Do you want to send to above user ? (y or n)")[0]
        if choice == 'n':
            print("Transaction stopped")
            return
        if len(receiverUserObject.linkedBankAccounts) == 0:
            print("User didn't linked any bank accounts")
            return
        amountToBeSent = int(input("Enter the amount to be sent: "))
        position = 1 
        for bank in user.linkedBankAccounts:
            print(position, " - ", bank.bankName)
            position += 1 
        option = int(input("Choose the bank number"))
        option -= 1 
        bankAccount = user.linkedBankAccounts[option]
 
        if bankAccount.balance >= amountToBeSent:
            bankAccount.balance -= amountToBeSent
            receiverUserObject.defaultBankAccount.balance += amountToBeSent
 
            transaction = Transaction()
            transaction.amountSent = amountToBeSent 
            transaction.senderName = user.fullName 
            transaction.receiverName = receiverUserObject.fullName 
            transaction.senderBankName = bankAccount.bankName 
            transaction.receiverBankName = receiverUserObject.defaultBankAccount.bankName
 
            user.previousTransactions.append(transaction)
            receiverUserObject.previousTransactions.append(transaction)
 
            print(amountToBeSent, " sent successfully") 
        else:
            print("Insufficient funds")
 
    def handlePrintPreviousTransactions(self, user):
        if len(user.previousTransactions) == 0:
            print("No transactions done yet")
            return 
 
        position = 1
        for transaction in user.previousTransactions[::-1]:
            print(position, ":")
            print("Amount sent: ", transaction.amountSent)
            print("Sender name: ", transaction.senderName)
            print("Receiver name: ", transaction.receiverName)
            print("Sender bank name: ", transaction.senderBankName)
            print("Receiver bank name: ", transaction.receiverBankName)
            print("\n\n")
            position += 1
 
    def handleSelfTransfer(self, user):
        if len(user.linkedBankAccounts) <= 1:
            print("Multiple accounts are not present")
            return 
        amountToTransfer = int(input("Enter the amount to transfer: "))
 
        position = 1 
        for bank in user.linkedBankAccounts:
            print(position, " - ", bank.bankName)
            position += 1 
        option1 = int(input("Choose the bank number (sender)"))
        option1 -= 1 
 
        option2 = int(input("Choose the bank number (receiver)"))
        option2 -= 1
        bankAccount1 = user.linkedBankAccounts[option1]
        bankAccount2 = user.linkedBankAccounts[option2]
        if bankAccount1.balance >= amountToTransfer:
            bankAccount1.balance -= amountToTransfer 
            bankAccount2.balance += amountToTransfer
 
            transaction = Transaction()
            transaction.amountSent = amountToTransfer 
            transaction.senderName = user.fullName 
            transaction.receiverName = user.fullName 
            transaction.senderBankName = bankAccount1.bankName 
            transaction.receiverBankName = bankAccount2.bankName
 
            user.previousTransactions.append(transaction)
            print("Transferred Successfully")
        else:
            print("Insufficient funds")
 