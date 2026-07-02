import random
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
while True:
    print('1. Finger Cricket\n2. Odd Even\n3. Number Guessing\n4. Rock Paper Scissors')
    choice=int(input('which game do you want to play?'))
    if choice==1:
        finger_cricket()
    elif choice==2:
        odd_even()
    elif choice==3:
        number_guessing()
    elif choice==4:
        rock_paper_scissors()
    else:
        print('Invalid choice')