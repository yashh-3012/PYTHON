import random
# SOME RANDOM GAMES JUST FOR REVISION OF MY 12TH 
def finger_cricket():
    c=0  
    while True:
        a=random.randint(1,6)
        b=int(input('enter batting number'))
        if b>6 or b<1:
            print('number invalid')
            continue
        if a==b:
            print('OUT!!!\n','Your total score is:',c)
            break
        else:
            c+=b
def odd_even():
        choice=input('Enter your choice (odd/even): ')
        if choice.lower() not in ['odd','even']:
            print('Invalid choice')
            return
        a=random.randint(1,6)
        b=int(input('enter your number'))
        c=a+b
        if c%2==0:
            y='even'
        else:
            y='odd'
        if choice.lower()==y:
            print('YOU WIN !!!\n','Computer\'s number:',a,'Your number:',b,'Result:',c)
        else:
            print('YOU LOSE !!!\n','Computer\'s number:',a,'Your number:',b,'Result:',c)
def number_guessing():
    number=random.randint(1,100)
    attempts=0 
    while True: 
        if attempts==5:
            print('YOU LOST!!!\nYou have used all your attempts.')
            break
        guess=int(input('Guess the number between 1 and 100: '))
        attempts+=1
        if guess<1 or guess>100:
            print('Number out of range')
            continue
        if guess<number:
            print('Too low!')
        elif guess>number:
            print('Too high!')
        if guess!=number:
            print('Try again!')
    if guess==number:
        print('Congratulations! You guessed the number in',attempts,'attempts.')
    else:
        print('The number was:',number)
def rock_paper_scissors():
    choices=['rock','paper','scissors']
    computer_choice=random.choice(choices)
    user_choice=input('Enter your choice (rock/paper/scissors): ')
    if user_choice.lower() not in choices:
        print('Invalid choice')
        return
    print('Computer\'s choice:',computer_choice)
    if user_choice.lower()==computer_choice:
        print('It\'s a tie!')
    elif (user_choice.lower()=='rock' and computer_choice=='scissors') or (user_choice.lower()=='paper' and computer_choice=='rock') or (user_choice.lower()=='scissors' and computer_choice=='paper'):
        print('You win!')
    else:
        print('You lose!')
# USED TIME MODULE TO GET THE CURRENT TIME AND GREET THE USER ACCORDINGLY
import time
def Time():
    t=time.strftime('%H:%M:%S')
    print('It\'s',t)
    T=int(time.strftime('%H'))
    if T>=4 and T<12:
        print('good morning')
    elif T>12 and T<16:
        print('Good Afternoon')
    elif T>16 and T<20:
        print('Good Evening')
    else:
        print('Good Night')
def reverse_num():
    n=int(input('Enter a number: '))
    c=0
    while n>0:
        s=n%10
        c=c*10+s
        n//=10
    print('Reversed number:',c)
def check_palindrome():
    n=input('Enter the entity to check if it is a palindrome: ')
    if n.isdigit():
        n=int(n)
        o=n
        r=0
        while n>0:
            s=n%10
            r=r*10+s
            n//=10
        if o==r:
            print('The number is a palindrome')
        else:
            print('The number is not a palindrome')
    else:
        n=n.lower()
        if n==n[::-1]:
            print('The string is a palindrome')
        else:
            print('The string is not a palindrome')
def voting():
    print('Welcome to the voting system \n To whom you want to vote for? \n 1.Yash\n2. Dewansh')
    v=int(input('Enter your voting choice: '))
    match v:                                        #match case statements
        case 1:
            print('You have voted for Yash')
        case 2:
            print('You have voted for Dewansh')
def do_while():
    while True:
        a=input('Enter your string: ')
        print(a)
        if a.islower():
            print('loop breaked because you entered a lowercase string')            
            break
def additon(*numbers):                      # arbitrary arguments(variable length argument) process as tuple 
    print(type(numbers))
    sum=0
    for i in numbers:
        sum+=i
    print('The sum of the numbers is:',sum)
def check_ap(**numbers):                        # keyword arbitrary arguments(variable length argument) process as dictionary
    print(type(numbers))
    if numbers['b']-numbers['a']==numbers['c']-numbers['b']:
        print('The numbers are in AP')
    else:
        print('The numbers are not in AP')
def listof_cubes():
    x=int(input('Enter starting value: '))
    y=int(input('Enter ending value: '))
    num=[i**3 for i in range(x,y+1)]
    print(num)
    for i in range(x,y+1):
        print('cube of',i,'is',i**3)
def KBC():
    price=0
    ques_ans=[['what is the capital of India?','new delhi'],['what is the full form of GDP?','gross domestic product'],['who is father of computer?','charles babagge']]
    print('Welcome to KBC!')
    for i in ques_ans:
        print(i[0])
        user_ans=input('Enter your answer: ')
        if user_ans.lower()==i[1].lower():
            print('Correct answer!')
            price+=1000
        else:
            print('Incorrect answer! The correct answer is:',i[1])
            break
    print('Your total prize money is:',price)
def fibonacci(n):
    '''returns a list of fibonacci series upto n terms'''           #doc string
    if n<=1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)                      #recursion statement
def set_methods():
    s1={1,2,3,4,5}
    s2={4,5,6,7,8}
    print('Union:',s1.union(s2))                                     # in simple word this func add boths sets and prints all unique elements
    print('Intersection:',s1.intersection(s2))                       #it prints the common elements in both sets
    print('Difference:',s1.difference(s2))                           # it removes the common elements from s1 
    print('Symmetric Difference:',s1.symmetric_difference(s2))       # it removes the common elements from both sets 
    print('Is s1 a superset of s2?',s1.issuperset(s2))               # it checks if s1 is a superset of s2 or not
    s1.add(6)                                                        # add a new element
    print('After adding 6 to s1:',s1)
    s1.remove(3)                                                     # removes the given element
    print('After removing 3 from s1:',s1)
def square_root():
    import math 
    try:                                                            #try block is used to test a block of code for errors
        x=int(input('Enter a number: '))
        print(f'Square root of {x} is {math.sqrt(x)}')
    except Exception as e:                                          #except block is used to handle the error 
        print(e)                                                    # e is the error that has occured
        print('end of the code')
    finally:                                                        #finally block it is executed wether error occured or not 
        print('i am inside finally block i am always executed')
def sq_func():
    print(' What is the range of the f(x)=x^2')
    r=int(input("enter the range :"))
    if r<0:
        raise ValueError(f'{r} DOESN\'T FALL IN THE RANGE')          # raise keyword is used to raise an error
    else:
        print(f'{r} Falls in the range of f(x)')
def word_guessing():
    l=['yash','hello','dewansh','india','google']
    hint=['my name','greeting starts from h','my friend\'s name','country name ends with a','one of the top tech company']
    w=''.join(random.choice(l).split())
    if w=='yash':
        print(hint[0])
    elif w=='hello':
        print(hint[1])
    elif w=='dewansh':
        print(hint[2])
    elif w=='india':
        print(hint[3])
    else:
        print(hint[4])    
    print('your word has',len(w),'letters')
    guessed_letters = []
    guess=0
    while True:
        if guess==10:
            print('all guesses are over')
            break
        x=input('enter the letter')
        guess+=1
        if x in w:
            guessed_letters.append(x)
            display:str= "".join(x if x in guessed_letters else "_" for x in w)
            print(display)
        if display == w:
            print('you guessed the word')
            break
while True:
    print('1. Finger Cricket\n2. Odd Even\n3. Number Guessing\n4. Rock Paper Scissors\n5.Time\n6. Reverse Number\n7. Check Palindrome\n8.Voting_System\n9. Do-While\n10. Addition\n11. Check AP\n12. List of Cubes\n13. KBC\n14. Fibonacci Series\n 15. Set Methods\n16. square root of a no.\n17. square function\n18.word guessing\n19. Exit')
    choice=int(input('enter your choice'))
    if choice==1:
        finger_cricket()
    elif choice==2:
        odd_even()
    elif choice==3:
        number_guessing()
    elif choice==4:
        rock_paper_scissors()
    elif choice==5:
        Time()
    elif choice==6:
        reverse_num()
    elif choice==7:
        check_palindrome()
    elif choice==8:
        voting()
    elif choice==9:
        do_while()
    elif choice==10:
        numbers=eval(input('Enter numbers separated by commas: '))
        additon(*numbers)
    elif choice==11:
        numbers=eval(input('Enter three numbers a, b, c in dictionary format'))
        check_ap(**numbers)   
    elif choice==12:
        listof_cubes()
    elif choice==13:
        KBC()
    elif choice==14:
        n = int(input("Enter the no. of terms you want to print: "))
        l = []
        for i in range(n):
            l.append(fibonacci(i))
        print(l)
        print(fibonacci.__doc__)
    elif choice==15:    
        set_methods()
    elif choice==16:    
        square_root()
    elif choice==17:
        sq_func()
    elif choice==18:
        word_guessing()
    elif choice==19:    
        print('Exiting the program...')
        break
    else:
        print('Invalid choice')