def show_menu():
    print("1. Answer a riddle")
    print("2. Add a riddle")
    print("3. Exit game")
    
    option = input("Enter option: ")
    return option
    
def add_question():
    print("")
    question = input("Enter a riddle\n> ")
    
    print("")
    print("Ok then, tell me the answer")
    answer = input("{0}\n> ".format(question))
    
    file = open("riddles.txt", "a")
    file.write(question + "\n")
    file.write(answer + "\n")
    file.close()
    
def game_loop():
    while True:
        option = show_menu()
        if option == "1":
            print("You selected 'Answer a riddle'")
        elif option == "2":
            add_question()
        elif option == "3":
            break 
        else:
            print("Invalid option")
        print("")
    
game_loop()