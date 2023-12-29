# Homework: BMI # 1
currentMode = 1
if currentMode == 0:
    inputX = input("Enter your height: ")
    inputY = input("Enter your weight: ")
    x = eval(inputX) / 100
    y = eval(inputY)

    bmi = y / (x * x)

    if bmi < 19.0:
        print("BMI is %2f, 體重太輕" % bmi)
    elif 19.0 <= bmi < 25.0:
        print("BMI is %2f, 體重適當，請繼續保持！" % bmi)
    elif bmi > 25.0:
        print("BMI is %2f, 體重過重！" % bmi)

# Homework: 九九乘法表 # 2
elif currentMode == 1:
    for i in range(1, 10):
        for j in range(1, 10):
            print("%2d x %2d = %2d" % (i, j, i * j), end="  ")
        print()
