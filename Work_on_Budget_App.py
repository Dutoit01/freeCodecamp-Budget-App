class Category():
  name = ""

  def __init__(self, nam):
      self.name = nam
      self.amount = 0
      self.ledger = []

  def deposit(self, amount, description="") : #deposit method
    self.amount = self.amount + amount #I will track the ledger balance using self.amount rather than adding ledger entries
    self.description = description
    self.ledger.append({"amount": amount, "description": description})#The ledger will include a list of repeated keys

  def withdraw(self, amount, description="") : #withdraw method
    if self.check_funds(amount) == False :
      return False 
    else :
      self.amount = self.amount - amount
      self.description = description
      amount = -amount #must store withdraw as a negative number
      self.ledger.append({"amount": amount, "description": description}) 
      return True

  def get_balance(self): #get_balance method
      return self.amount

  def transfer(self, amount, otherbud): #transfer method
    if (isinstance(otherbud, Category) and self.check_funds(amount)) == True : #Also protects against false budget entries
        otherbud.deposit(amount, "Transfer from " + self.name)
        self.withdraw(amount, "Transfer to " + otherbud.name)
        return True
    elif isinstance(otherbud, Category) != True :
        print("Please enter a valid budget category")
        return False
    else:
        print("Insufficient funds")
        return False

  def check_funds(self, amount):   #check_funds method
    if amount > self.amount:
        return False
    else :
        return True

  def __str__(self): #To make the object print the required way
    if len(self.name) % 2 == 0 : #I have 30 spaces per line and have to centre the title between stars
        right = (30 - len(self.name)) / 2 #if the name is an even #characters then I split stars equally
        left = right
    else :
        right = (30 - len(self.name) -1) / 2 #if uneven number of stars needed, then I put the extra star on the left
        left = right + 1 
    header = self.name #will call the first name header
    for i in range(int(left)) : #gives stars to the left of title
        header = "*" + header
    for i in range(int(right)) : #gives stars to the right of title
        header = header + "*"
    header = header + "\n" #this will move us to the next line without a space
    descri_block = "" #this will be the block of text under the string that I will iteratively fill below
    for i in range(len(self.ledger)) : #gives lines in object printout
        lefty = self.ledger[i]["description"] #gives me the description from the ledger
        righty = str(self.ledger[i]["amount"])
        if "." in righty: 
          if len(righty[righty.find("."):]) == 2:
            righty = righty + "0" #only one decimal so add 0
        else :
            righty = righty + ".00"
        edlefty = lefty[0:23] #the first 23 letters of the description is selected
        edrighty = righty[0:6]
        spaces = 30 - len(edlefty) - len(edrighty) #need a total of thirty spaces
        for k in range(spaces) :
            edlefty = edlefty + " " #add spaces needed between description and amount to description
        line = edlefty + edrighty + "\n"
        descri_block = descri_block + line
    final = "Total: " + str(self.amount) #the final line showing category balance
    block = header + descri_block + final
    return block

def create_spend_chart(budgets): #the create_spend_chart function
    withdrawals = [] #because I stored the withdrawals as strings to be able to format them right, I have to convert them back to floats here
    total = 0 #to calculate the percentages
    names = [] #I'll collect the names of the budget category for later display
    for budget in budgets: #I have to account for every budget category
        withdraw = 0
        for i in range(len(budget.ledger)) :
            if "-" in str(budget.ledger[i]["amount"]): #selects only the withdrawals in the ledger
                withdraw = withdraw + float(budget.ledger[i]["amount"]) #I don't need indiv withdrawals: only total
        withdrawals.append({budget.name: withdraw}) #list of dictionaries with budget keys and withdraw vals
        total = total + withdraw
        names.append(budget.name)
    percs = [] #Here I will assign the list of dictionaries with the percentage spending of budgets
    rawnum = [] #Here I will assign simply the percentages without keys
    for budget in budgets:
        for i in range(len(withdrawals)):
            if budget.name in withdrawals[i]:
                perc = float(withdrawals[i][budget.name]) #gives the percentage for each budget name
                perc = perc/total * 100
                perc = round(perc/10)*10 #I only need the percentages rounded to the nearest 10
                percs.append({budget.name : perc}) #list of dictionaries with names and percentages
                rawnum.append(perc)
    number = [] #list of 0 to 100 percentages
    for i in range(11):
        if i == 0:
            number.append("  " + str(i) + "|")
        elif i < 10:
            number.append(" " + str(i*10) + "|")
        else :
            number.append(str(i*10) + "|")            
    #this is the list of horizontal labels.
    histhead = "Percentage spent by category\n" #header for histogram 
    hist= "" #contstructing the histogram
    hist = histhead + hist
    empty= "          " #10 spaces for when there are no percentages as large as a certain value
    omidleft = " o " #the leftmost and center columns take three space. o implies "o" present
    oright = " o  " #the right column takes four spaces.
    midleft = "   " #provides three spaces
    right = "    " #provides four spaces
    maxim = max(rawnum)/10
    minim = min(rawnum)
    if minim != 0:
        minim = min(rawnum)/10
    if maxim < 10: #in the case that no category has all the spending, we know that the histogram will have empty lines
        for i in range(10, int(maxim), -1):
            hist = hist + number[i] + empty + "\n"
    for i in range(int(maxim), int(minim), -1): #between the maximum and minimum percentages, some categories may have empty bars and others full. This assesses.
        for j in range(len(rawnum)):
            if j == 0 and rawnum[j] != 0: #j=0 is leftmost column: have to add the percentage from number differently
                if rawnum[j]/10 >= i: #as long as rawnum[j]/10 is greater than the current index, we know we have to add an o
                    hist = hist + number[i] + omidleft
                else :
                    hist = hist + number[i] + midleft
            elif j > 0 and j < (len(rawnum)-1) and rawnum[j] != 0: #avoids dividing by ten in case of a 0 percent
                if rawnum[j]/10 >= i:
                    hist = hist + omidleft
                else:
                    hist = hist + midleft
            elif j > 0 and j < (len(rawnum)-1) and rawnum[j] == 0: #if we have a 0 percent category, we need to explicitly deal with it.
                hist = hist + midleft #no o added since 0 percent
            else :
                if rawnum[j] != 0:
                    if rawnum[j]/10 >= i:
                        hist = hist + oright + "\n"
                    else:
                        hist = hist + right + "\n" 
                else:
                    hist = hist + right + "\n" #if rightmost category is a 0 percent, we add no o.
    for i in range(int(minim), -1, -1): #Here, everythins is below the minimum line: all percentages have at least this many percentages. We add o to all
        #As such, code is same as above, but without checking for sufficient size
        for j in range(len(rawnum)):
            if j == 0 and rawnum[j]/10 > i:
                hist = hist + number[i] + omidleft
            elif j==0 :
                hist = hist + number[i] + midleft
            if j > 0 and j < (len(rawnum)-1) and rawnum[j] != 0:
                hist = hist + omidleft
            elif j > 0 and j < (len(rawnum)-1):
                hist = hist + midleft
            if j == (len(rawnum)-1) :
                if rawnum[j] != 0:
                    hist = hist + oright + "\n"
                else:
                    hist = hist + right + "\n" 
    bottom_line = "    " #line between histogram and labels. starts with 4 spaces and has 3 dashes per category except the last which has 4
    threed = "---" #the dashes to be added 
    fourd = "----"
    for i in range(len(rawnum)):
        if i < (len(rawnum)-1):
            bottom_line = bottom_line + threed
        else :
            bottom_line = bottom_line + fourd + "\n"
    hist = hist + bottom_line #adds the dashes
    linecat = "" #The bottom part. Start with 5 spaces then letter, then two spaces, the letter... then lastly two spaces
    for i in range(len(max(names, key = len))): #sets up the for loop to run for max length category name
       linecat = linecat + right #every line starts with four spaces plus one below
       if i < (len(max(names, key = len))-1) :
           for j in range(len(names)): #ranges over names 
               if j < (len(names)-1):
                   try : 
                       linecat = linecat + " " + names[j][i] + " "#from name j we take ith letter, if pressent. Otherwise space
                   except :
                        linecat = linecat + midleft #midleft = 3spaces
               else :
                   try : 
                       linecat = linecat + " " + names[j][i] + "  \n"#from name j we take ith letter, if pressent. Otherwise space
                   except :
                        linecat = linecat + right + "\n" #right = 4 spaces
       else :
           for j in range(len(names)): #ranges over names 
               if j < (len(names)-1):
                   try : 
                       linecat = linecat + " " + names[j][i] + " "#from name j we take ith letter, if pressent. Otherwise space
                   except :
                        linecat = linecat + midleft #midleft = 3spaces
               else :
                   try : 
                       linecat = linecat + " " + names[j][i] + "  "#from name j we take ith letter, if pressent. Otherwise space
                   except :
                        linecat = linecat + right #right = 4 spaces
    
    hist = hist + linecat
    return hist