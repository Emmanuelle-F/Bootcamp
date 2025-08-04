# Given a valid (IPv4) IP address, return a defanged version of that IP address.

# A defanged IP address replaces every period "." with "[.]".

# proper format: x.x.x.x
# value between 0 and 255
# no leading 0 Ex: 01, 00


def checkIpAdress(ipAddress):
    splittedIpAddress = ipAddress.split(".")
    errorMessage = ""

    if len(splittedIpAddress) == 4:
        
        for x in splittedIpAddress:

            if x.isdigit():
                

                if len(x) > 1 and x.startswith("0"):
                    errorMessage = "The IP Address should not have leading zeroes"
                else:

                    x_int = int(x)

                    if x_int < 0 or x_int > 255:
                        errorMessage = "The IP Address should contain only numbers between 0 and 255" 
                
            else:
                errorMessage = "The IP Address should contain only numbers"

    else:
        errorMessage = "The correct format is x.x.x.x"

    return errorMessage


def defangingIpAddress(ipAddress):
    return ipAddress.replace(".", "[.]")


while True:

    userInput = input("Please enter a valid IP (IPV4) address: ")

    validationMessage = checkIpAdress(userInput)

    if validationMessage == "":
        defangedIpAdress = defangingIpAddress(userInput)
        print("Defanged IP address:", defangedIpAdress)
        break
    else:
        print (f"Error Message: {validationMessage} ")

