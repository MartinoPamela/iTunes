from model.model import Model

mymodel = Model()
mymodel.buildGraph(120*60*1000)
print(mymodel.getGraphDetails())

mymodel.getNodeI(261)
#mymodel.getSetAlbum(mymodel.getNodeI(261), )
