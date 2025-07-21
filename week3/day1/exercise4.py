valid_flag = False
while not valid_flag:
    userage = input("How old are you?")
    try:    # TRY THIS
        userage    = int(userage)
    except: # IF YOU GOT AN ERROR
        print("Wrong age!")
    else:   # ELSE
        valid_flag = True
    finally:
        print('There may or may not have been an exception.')

print("Next year, your age will be",userage+1)
