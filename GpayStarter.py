from GpayController import * 
 
 
obj = GpayController()
 
while True:
    print("\n\n\n***********************************")
    print("1 - Signup")
    print("2 - Login")
    print("3 - Exit")
    print("***********************************")
    option = int(input("Choose your preferred option:"))
 
    if option == 1:
        obj.handleSignup()
    elif option == 2:
        obj.handleLogin()
    elif option == 3:
        print("Thank you for using G-Pay!!!")
        exit(0)
    else:
        print("Select appropriate option")