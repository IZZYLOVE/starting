import requests
import json
import re
def convert(*args): # Using args to be able to catch and handle some errors to avoid throwing raw errors to the user
    args = args
    fname = c_from = c_to = amount = ''
    lenargs = len(args)# Since the required arquments must be three or four
    if lenargs < 3 or lenargs > 4 :# check if parameters are less than three or greater than four
        print("Please enter three or four parameters!")
        check_args = 'no'
    else: # The length of parameter is three or four
        try: # Check if the first parameter is a number
            amount = float(args[0])
            check_args = 'ok'
        except:
            print('The first parameter should be a number')
            check_args = 'no'

        if check_args == 'ok': # Catch the other two/three parameters
            c_from = str(args[1]).upper()
            c_to = str(args[2]).upper()
            try:  # Since the last parameter is not required
                fname = str(args[3])
            except:
                fname = ''

        # Validating c_from and c_to using regular expression to ensure they are natural and matching strings
        pattern0 = re.compile(r'^[-_*&%$#@!~+=]')
        pattern1 = re.compile(r'[0-9-_*&%$#@!~+=]')
        pattern2 = re.compile(r'[*&%$#@!~+=]')
        matches1 = pattern1.finditer(c_from)
        matches2 = pattern1.finditer(c_to)
        matches3 = pattern0.finditer(fname)
        m1=''
        for match in matches1:
            m1=f"{m1} {match}"
        if m1 == '':
            check_args = 'ok'
        else:
            check_args = 'no'
            print(f'{c_from} matches not ok, only three letters required')

        if check_args == 'ok':
            m2 = ''
            for match in matches2:
                m2 = f"{m2} {match}"
            if m2 == '':
                check_args = 'ok'
            else:
                check_args = 'no'
                print(f'{c_to} matches not ok, only three letters required')

        if check_args == 'ok' and fname !='':
            m3=''
            for match in matches3:
                m3 = f"{m3} {match}"
            if m3 == '':
                check_args = 'ok'
            else:
                check_args = 'no'
                print(f'{fname} matches not ok, special character should not begin a file name')

    if check_args == "ok":
        if len(c_from) != 3:
            check_args = 'no'
            print(f'{c_from} matches not ok, only three letters required')

    if check_args == "ok":
        if len(c_to) != 3:
            check_args = 'no'
            print(f'{c_to} matches not ok, only three letters required')

    if check_args == "ok": # If parameters are ok, we initiate the API sequence in a try block to catch possible errors
        key = 'UMMiEijAVJWnx3BCLZwSockJeM7qfCcd'
        header = {'apikey': key}
        payload = {}
        try:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={c_to}&from={c_from}&amount={amount}"
            response = requests.get(url, headers=header, data=payload)
            datastats = response.status_code
            if datastats >= 600:
                print(f'{datastats}, E600+ processing error!')
            elif datastats >= 500:
                print(f'{datastats}, Server error!')
            elif datastats >= 400:
                print(f'{datastats}, Client server error!')
            elif datastats >= 300:
                print(f'{datastats}, Redirection response error!')
            elif datastats >= 200:
                data = response.json()
                print("\n")
                checkerror = data.get('error')  # Using .get query method to get response of none instead of row error
                success = data.get('success')  # Using .get query method to get response of none instead of row error
                if data == '':  # Check if returned response is empty
                    print(f"{datastats}, Suspected empty response!")
                elif success == True:  # Check if response is success
                    if fname != '':  # Formatting file name and generating write or not switch
                        filename = f"{fname}.txt"
                        write = 'on'
                    else:
                        filename = ''
                        write = 'off'
                    input_parameters = data['query']
                    info_parameters = data['info']
                    result_parameters = data['result']
                    date_parameters = data['date']
                    mytxt = "YOUR INPUT PARAMETERS ARE AS FOLLOWS: "
                    print(mytxt)
                    Mytxt = f"{mytxt}"  # Adding/appending evey print statement to a variable, to write when ready
                    for key, value in input_parameters.items():
                        mytxt = f"{key}: {value}"
                        print(mytxt)
                        Mytxt = f"{Mytxt} \n{mytxt}"

                    mytxt = "\nYOUR INFO PARAMETERS ARE AS FOLLOWS: "
                    print(mytxt)
                    Mytxt = f"{Mytxt} \n{mytxt}"

                    for key, value in info_parameters.items():
                        mytxt = f"{key}: {value}"
                        print(mytxt)
                        Mytxt = f"{Mytxt} \n{mytxt}"

                    mytxt = f"result: {result_parameters} "
                    print(mytxt)
                    Mytxt = f"{Mytxt} \n{mytxt}"

                    mytxt = f"date: {date_parameters} "
                    print(mytxt)
                    Mytxt = f"{Mytxt} \n{mytxt}"

                    if write == 'on':  # Using the write or not switch to write if the switch is on/(file name is given)
                        with open(filename, 'w') as file_object:  # file write block
                            file_object.write(str(Mytxt))

                elif checkerror != 'None':
                    check_message = data['error'].get('message')
                    print(f"{check_message}")

            elif datastats >= 0:
                print(f'{datastats},Informational response error!')
            else:  # Unknown error
                print(f'{datastats}, negative processing error!')

        except:# If no error in the try block is hit then there is no internet connection
            print(f"... Please check your internet connection ...!")

def initiator(): # This is to act as user interface
    amountx = input("Enter amount: ")
    try:
        amount = float(amountx)
        c_from = input("Enter the current currency: ").upper().strip()
        c_to = input("Enter the desired currency: ").upper().strip()
        fname = input("Enter file name (not required): ").strip()
        convert(amount, c_from, c_to, fname)
    except:
        print('Please enter a number')
        initiator()
initiator() # Caling the (user interface) initiator class
