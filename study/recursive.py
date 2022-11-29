def countdown(num):
    if num == 0:
        print("end")
    else:
        print(num)
        countdown(num-1)

countdown(10)