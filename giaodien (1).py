from tkinter import *
import csv
import numpy as np
import math
import array as arr

def loadData(path):
    f = open(path, "r")
    data = csv.reader(f)
    data = np.array(list(data))
    data = np.delete(data, 0, 0)
    data = np.delete(data, 0, 1)
    np.random.shuffle(data)
    f.close()
    trainSet = data[:100]
    testSet = data[100:]

    return trainSet, testSet


def calcDistancs(pointA, pointB, numOfFeature=4):
    tmp = 0
    for i in range(numOfFeature):
        tmp += (float(pointA[i]) - float(pointB[i])) ** 2
    return math.sqrt(tmp)

def kNearestNeighbor(trainSet, point, k):
    distances = []
    for item in trainSet:
        distances.append({
            "label": item[-1],
            "value": calcDistancs(item, point)
        })
    distances.sort(key=lambda x: x["value"])
    labels = [item["label"] for item in distances]
    return labels[:k]

def findMostOccur(arr):
    labels = set(arr)
    ans = ""
    maxOccur = 0
    for label in labels:
        num = arr.count(label)
        if num > maxOccur:
            maxOccur = num
            ans = label
    return ans



def main():
    trainSet, testSet = loadData("./lungcancer.csv")
    numOfRightAnwser = 0
    age = int(Age.get())
    smokes = int(Smokes.get())
    areaq = int(AreaQ.get())
    alkhol = int(Alkhol.get())
    for item in testSet:
        knn = kNearestNeighbor(trainSet, item, 3)
        answer = findMostOccur(knn)
        numOfRightAnwser += item[-1] == answer
        print("label: {} -> predicted: {}".format(item[-1], answer))




    print("Accuracy", (numOfRightAnwser/len(testSet))*100 )
    sample = trainSet
    point = arr.array('i', [age, smokes, areaq, alkhol])
    print(point)
    result1 = kNearestNeighbor(sample, point, 3)
    print(result1) #Neighbor
    result2 = findMostOccur(result1)
    print(result2[0])
    if result2[0] == '0':
        notification.insert(INSERT,"Patient without lung cancer")
    elif result2[0] == '1':
        notification.insert(INSERT, "Patient with lung cancer")

window = Tk()
window.title("Lung Canner")
window.geometry("600x200")
window.config(bg='lavender')
window.resizable(False,False)
Label(window, text='Enter Age',bg='lavender').grid(row=0,column=0)
Label(window, text='Enter Smokes',bg='lavender').grid(row=1,column=0)
Label(window, text='Enter AreaQ',bg='lavender').grid(row=2,column=0)
Label(window, text='Enter Alkhol',bg='lavender').grid(row=3,column=0)
Age = Entry(window,width=15)
Age.grid(row=0,column=1)
Smokes = Entry(window,width=15)
Smokes.grid(row=1,column=1)
AreaQ = Entry(window,width=15)
AreaQ.grid(row=2,column=1)
Alkhol = Entry(window,width=15)
Alkhol.grid(row=3,column=1)
Button(window,text='Process',bg='skyblue',command=main).grid(row=6,column=0)
notification = Text(window,height=1,width=30)
notification.grid(row=5,column=1)
window.mainloop()