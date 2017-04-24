import networkx
import csv


class Item:
    def __init__(self, filmName, actorName):       
        super().__init__()
        self.filmName = filmName
        self.actorName = actorName    


def Graph(items):
    ## Check if film is in the list, if not, add, and asociate with actors
    filmAsocActors = {}  
    graph = networkx.Graph()
    for item in items:
        graph.add_node(item.actorName)
        ## Check
        if item.filmName in filmAsocActors:            
            filmAsocActors[item.filmName].append(item.actorName)
        else:
            filmAsocActors[item.filmName] = []
            filmAsocActors[item.filmName].append(item.actorName)

    for film, actor_list in filmAsocActors.items():
        ## just less than 5 actors
        if len(actor_list) > 5: 
            continue

        for actorA in actor_list:
            for actorB in actor_list:
                if actorA != actorB:
                    graph.add_edge(actorA, actorB)

    return graph

## Read data
data = []
with open('casts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        data.append(row)

items = []
for row in data:
    items.append(Item(row[1], row[2]))
print("Count of items: ", len(items))
graph = Graph(items)

## Statistics
print("######################")
print("Statistics:")
print("# nodes: ", graph.number_of_nodes())
print("# edges: ", graph.number_of_edges())
print("components: ", networkx.number_connected_components(graph) )
print("density: ", graph.number_of_edges() / (graph.number_of_nodes() * (graph.number_of_nodes() - 1) / 2))
print("######################")

##Bacon

LenCnt = 0    
LenSum =0 
selected_player='Barbara Hershey'
lengths = networkx.single_source_shortest_path_length(graph, selected_player)

for act in graph.nodes():
    graph.node[act]['BaconLen'] = -1

for act, Len in lengths.items():
    graph.node[act]['BaconLen'] = Len
    LenCnt = LenCnt + 1
    LenSum = LenSum + Len


LenSort = sorted(lengths.items(), key=lambda element: element[1], reverse=True)
print("######################")
print("Bacon Stat")
print("Average: ", LenSum / LenCnt)

print("/nTen highes:")
for actorlen in LenSort[:10]:
    print(actorlen[0], " ",actorlen[1])

print("Ten lowest:")
for actorlen in LenSort[-10:]:
    print(actorlen[0], " ",actorlen[1])

print("######################")


##Communities
communities = {}
for id, community in enumerate(networkx.k_clique_communities(graph, 3)):
    for i in community:
        communities[i] = id + 1

# make groups of acters
commActors = {}
for key, val in communities.items():
    if val not in commActors:
        commActors[val] = []
    commActors[val].append(key)

# biggest communities
commActors_sorted = sorted(commActors.items(), key=lambda a: len(a[1]), reverse=True)

print("######################")
print("Communities:")
for community in commActors_sorted[:5]:
    print("# actors:", len(community[1]), community[1])
print("######################")

for act, id in communities.items():
    graph.node[act]['id'] = id

##Centralities
##choosed centrality 
centralities = [ networkx.degree_centrality]

print("######################")
for centrality in centralities:
    centrality_res = centrality(graph)

    for act, centrality_val in centrality_res.items():
        graph.node[act]['Degree Centrality'] = centrality_val

    centralitySort = sorted(centrality_res.items(), key=lambda element: element[1], reverse=True)
    print("Degree Centrality / TOP TEN ")
    for act in centralitySort[:10]:
        print(act[0], "value:", act[1])

print("######################")

networkx.write_gexf(graph, 'export.gexf')


