import os
from ply2stl import Ply2Stl


pp = Ply2Stl()
for ply in os.listdir("./data1"):
    print ply
    #with open("./data//" + ply) as f:
    #	content = f.read().replace(",", ".")
    #with open("./data1//" + ply, "w") as f:
    #	f.write(content)	 
    pp.addToStl("./data1//" + ply)
pp.finishStl("./resultscan.stl")
