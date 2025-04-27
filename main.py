#GroceryStoreSim.py
#Name:
#Date:
#Assignment:

import simpy
import random

eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items // 2  # shopping takes 1/2 a minute per item
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)  # wait a minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

def customerArrival(env, arrival_interval):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(arrival_interval)  # New shopper every 'arrival_interval' minutes

def processResults():
    totalWait = 0
    totalShoppers = 0
    waitTimes = []

    for e in eventLog:
        waitTime = e[4] - e[3]  # depart time - done shopping time
        waitTimes.append(waitTime)
        totalWait += waitTime
        totalShoppers += 1

    avgWait = totalWait / totalShoppers
    maxWait = max(waitTimes)
    minWait = min(waitTimes)

    print("The average wait time was %.2f minutes." % avgWait)
    print("The maximum wait time was %.2f minutes." % maxWait)
    print("The minimum wait time was %.2f minutes." % minWait)
    print("The total number of shoppers served was %d" % totalShoppers)
    print("The total idle time was %d minutes" % idleTime)

def main():
    numberCheckers = 5       # you can change this (example: 2, 3, 5, 10)
    arrival_interval = 2     # shopper arrives every 2 minutes (you can change it too)

    env = simpy.Environment()

    env.process(customerArrival(env, arrival_interval))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180)  # run for 3 hours (180 minutes)

    print(len(waitingShoppers), "shoppers still waiting at the end.")
    processResults()

if __name__ == '__main__':
    main()
