import random
import os

MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 1

ROWS = 3
COLS = 3

bet_amounts = []
added_moneys = []

symbol_count = {
  "A": 2,
  "B": 4,
  "C": 6,
  "D": 8
}

symbol_value = {
  "A": 25,
  "B": 15,
  "C": 10,
  "D": 5
}

def check_winnings(columns, lines, bet, values):
  winnings = 0
  winning_lines = []
  for line in range(lines):
      symbol = columns[0][line]
      for column in columns:
          symbol_to_check = column[line]
          if symbol != symbol_to_check:
              break
      else:
          winnings += values[symbol] * bet
          winning_lines.append(line + 1)

  return winnings, winning_lines



def get_slot_machine_spin(rows, cols, symbols):
  all_symbols = []
  for symbol, symbol_count in symbols.items():
      for _ in range(symbol_count):
          all_symbols.append(symbol)

  columns = []
  for _ in range(cols):
      column = []
      current_symbols = all_symbols[:]
      for _ in range(rows):
          value = random.choice(current_symbols)
          current_symbols.remove(value)
          column.append(value)

      columns.append(column)

  return columns


def print_slot_machine(columns):
  for row in range(len(columns[0])):
    for i, column in enumerate(columns):
      if i != len(columns) - 1:
        print(column[row], end=" | ")
      else:
        print(column[row], end="")

    print()


def deposit():
  while True:

    amount = input("How much would you like to deposit? $")
    if amount.isdigit():
      amount = int(amount)
      if amount > 0:
        break
      else:
        print("Amount must be greater that 0.")
    else:
      print("Please enter a valid number")

  return amount

def num_of_lines():
  while True:
    print()
    print("New Ticket")
    print("------------------")
    lines = input("How many lines would like to bet on, 1-3? ")
    if lines.isdigit():
      lines = int(lines)
      if 1 <= lines <= 3:
        break
      else:
        print("Amount must be between 1-3.")
    else:
      print("Please enter a valid number")

  return lines

def get_bet():
  while True:
    bet = input("How much would you like to bet on each line? $")
    if bet.isdigit():
      bet = int(bet)
      if MIN_BET <= bet <= MAX_BET:
        break
      else:
        print(f"Amount must be between ${MIN_BET} and ${MAX_BET}. ")
    else:
      print("Please enter a valid number")

  return bet

def low_bal(balance):
  if balance < 50:
    print()
    if balance == 0:
      print("YOUR OUT OF MONEY")
    else:
      print("YOUR ALMOST OUT OF MONEY")
    print("---------------------")
  while balance < 50:
    
    added_money = input("You've almost, or have, run out of money, how much would you like to add? $")
    if added_money.isdigit():
        added_money = int(added_money)
        if added_money > 0:
            balance += added_money
            added_moneys.append(added_money)
            break
        else:
            print("Enter a number greater than 0.")
    else:
        print("Please enter a valid number")

  return balance



def spin(balance):
  lines = num_of_lines()

  #check if there is enough money for bet

  while True:
    bet = get_bet()
    total_bet = bet * lines
    if total_bet > balance:
      print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
    else:
      bet_amounts.append(total_bet)
      break

  print("")
  print("BET TICKET")
  print("------------------")
  print(f"You are betting ${bet} on {lines}x lines.: ${total_bet}" )
  print()

  slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
  print_slot_machine(slots)
  winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
  print()
  print("INFO")
  print("------------------")
  if winnings - bet > 0:
    print(f"You won ${winnings - bet}")
  else:
    print(f"You lost ${abs(winnings - (bet*lines))}")
  if winnings > 0:
    print(f"You won on line:", *winning_lines)
  
  return winnings - total_bet
  



def main():

  count = 0 
  balance = deposit()
  initial_bal = balance


  
  
  while True:
    balance = low_bal(balance)
    print(f"Your current balance is: ${balance}")
    print()
    answer = input("Press enter to play (q to quit)")
    if count > 0:
      os.system('clear')
    if answer == "q":
      break
    balance += spin(balance)

    count += 1

  #calculate values for end screen
  if count > 0:
    avg_bet = sum(bet_amounts)/len(bet_amounts)
  total_dif = (balance - sum(added_moneys)) - initial_bal
  

  #end screen
  print()
  print("STATS")
  print("-----------")
  print(f"You started with: ${initial_bal}")
  if sum(added_moneys) > 0:
    print(f"You added: ${sum(added_moneys)}")
  print(f"You left with: ${balance}")
  print(f"You played: {count} time(s)")
  if count > 0:
    print(f"Your average bet was ${avg_bet}")
  #print if the user lost or gained money
  if total_dif < 0:
    print(f"You lost $ {abs(total_dif)}")
  elif total_dif > 0: 
    print(f"You won ${abs(total_dif)}")
  else:
    print("You: Broke even")



main()
