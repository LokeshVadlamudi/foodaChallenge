import os
import json
import math
from datetime import datetime

class RewardCal:
    def __init__(self, inputFile, customerData, rewardSchedule):
        self.inputFile = inputFile
        self.customers = customerData
        self.rewardSchedule = rewardSchedule

    #fetch hours and mins from timestamp
    def getHourMins(self,x):
        date = datetime.fromisoformat(x)
        mins = str(date.minute)
        if len(mins) == 1:
            mins = '0' + mins
        return str(date.hour)+mins

    #register user into database and initializes rewards and orders
    def registerNewUser(self,name,customerTable):
        customerTable[name] = (0,0)
        return

    def processRewards(self):
        # Opening JSON file
        f = open(self.inputFile,)

        data = json.load(f)

        for i in data['events']:
            if i['action'] == 'new_customer':
                self.registerNewUser(i['name'],customers)
            else:
                customer = i['customer']
                previousRewards, previousOrders= customers[customer]
                orderTime = i['timestamp']
                hourMins = self.getHourMins(orderTime)
                hourMins = int(hourMins)

                #default rewards if time doesn't match with rewards schedule
                rewardMultiplier = (0.25/1)

                for k in rewardSchedule.keys():
                    minT , maxT = k
                    if minT <= hourMins <= maxT:
                        rewardMultiplier = rewardSchedule[k]
                        break
                totalRewards = math.ceil(i['amount'] * rewardMultiplier)
                #discarding the rewards that are less than 3 or greater than 20
                if totalRewards < 3 or totalRewards > 20:
                    continue
                customers[customer] = (previousRewards+totalRewards,previousOrders+1)
        
        f.close()
        return customers


    def writeOutputFile(self,fileName,customerDict):
        f = open(fileName,"w")
        for k,v in customerDict.items():
            totalRewards , orders = v
            if orders > 0:
                str1 = k + ': ' +  str(totalRewards) + ' points with ' + str(totalRewards / orders) + ' per order.'
                f.write(str1)
                f.write('\n')
            else:
                str2 = k + ': ' + 'No orders.'
                f.write(str2)
                f.write('\n')
        f.close()



#rewards dictionary

rewardSchedule = {
    (1200,1259) : (1/3),
    (1100,1159) : (1/2),
    (100,159) : (1/2),
    (1000,1059) : (1/1),
    (200,259) : (1/1),
}

#dictionary to store customers
customers = {}

#create the object
rc = RewardCal('input.json', customers, rewardSchedule)


#call the method to calculate the rewards
customerTable = rc.processRewards()

#write to a output file the results
rc.writeOutputFile('output.txt',customerTable)
    