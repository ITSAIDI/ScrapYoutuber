##################### Discription ###############################
# Sponsoring Companies can pass a long time searching for main informations about 
# a youtuber like (First and Last name, Main Topics, Email adresss, ...).
# Also they spend a lot of time comparing youtubers we can Automate all these process
# The Goals :
#------------ Featch The main informations about a Youtuber (First name, Email adrees, Instagram...)
#------------ Help Sponsores comparing youtubers.
from Functions import Visualize
from Tools import clear_database
from Graph import Graph




#Visualize(Graph)
#clear_database()
def main():
    Youtube_handle = "@aiadvantage"
    for event in Graph.stream({"Youtube_Handle":Youtube_handle,"Response":"None"}):
        for value in event.values():
            pass
main()






















