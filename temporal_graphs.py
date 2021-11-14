import matplotlib.pyplot as plt
from os import read
import networkx as nx
import json
import os

path = f"{os.getcwd()}\\tmp_dblp_coauthorship.json"

def read_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
        return data

def write_json(file_name, json_obj):
    with open(file_name, 'w') as f:
        f.write(json.dumps(json_obj, indent=4))

def get_gcc(g):
    print("Retrieving Giant Connected Component ...")
    g_cc = sorted(nx.connected_components(g), key=len, reverse=True)
    gc = g.subgraph(g_cc[0])
    return gc

def report_nodes_edges(g):
    print("Creating report ...")
    return {
        "number_of_nodes": g.number_of_nodes(),
        "number_of_edges": g.number_of_edges()
    }

def get_sorted_pagerank(g):
    pr = nx.pagerank(g)
    sorted_pr = {}
    sorted_keys = sorted(pr, key=lambda x:x[1], reverse=True)
    for k in sorted_keys:
        sorted_pr[k] = pr[k]
    
    return sorted_pr

def get_sorted_edge_betweeness(g, weighted):
    if (weighted):
        eb = nx.edge_betweenness_centrality(g, k=100, weight="weight")
    else:
        eb = nx.edge_betweenness_centrality(g, k=100)

    sorted_eb = {}
    sorted_keys = sorted(eb, key=lambda x:x[1], reverse=True)
    for k in sorted_keys:
        sorted_eb[k] = eb[k]

    return sorted_eb


def get_first_N(d, n):
    d_items = d.items()
    return list(d_items)[0:n]


print(f"Reading json from, {path}")
data = read_json(path)

### temporal graph a) ###

dblp_2005 = nx.Graph()
print("Generating graph dblp_2005 ...")
for t in data:
    n1, n2, year = t
    if (year == 2005):
        dblp_2005.add_edge(n1, n2)

gcc = get_gcc(dblp_2005)
report = report_nodes_edges(gcc)
print(report)

### temporal b) ###

dblp_2006 = nx.Graph()
print("Generating graph dblp_2006 ...")
for t in data:
    n1, n2, year = t
    if (year == 2006):
        dblp_2006.add_edge(n1, n2)

gcc = get_gcc(dblp_2006)
report = report_nodes_edges(gcc)
print(report)

### temporal c) ###

dblp_2005_w = nx.Graph()
print("Generating graph dblp_2005_w ...")
for t in data:
    n1, n2, year = t
    if (year == 2005):
        if (dblp_2005_w.has_edge(n1, n2)):
            dblp_2005_w[n1][n2]["weight"] += 1
        else:
            dblp_2005_w.add_edge(n1, n2, weight=1)

gcc = get_gcc(dblp_2005_w)
report = report_nodes_edges(gcc)
print(report)

### Node and Edge Importance in Graphs i) ###
print("Getting Page rank importance ...")
pr_dblp_2005 = get_first_N(get_sorted_pagerank(dblp_2005), 50)
pr_dblp_2006 = get_first_N(get_sorted_pagerank(dblp_2006), 50)
pr_dblp_2005_w = get_first_N(get_sorted_pagerank(dblp_2005_w), 50)
print("Writing results ...")
write_json("pr_dblp_2005.json", pr_dblp_2005)
write_json("pr_dblp_2006.json", pr_dblp_2006)
write_json("pr_dblp_2005_w.json", pr_dblp_2005_w)

### Node and Edge Importance in Graphs ii) ###
print("Getting Edge Betweeness importance ...")
#Probably need top run with k=1000
eb_dblp_2005 = get_first_N(get_sorted_edge_betweeness(dblp_2005, False), 20)
eb_dblp_2006 = get_first_N(get_sorted_edge_betweeness(dblp_2006, False), 20)
eb_dblp_2005_w = get_first_N(get_sorted_edge_betweeness(dblp_2005_w, True), 20)
print("Writing results ...")
write_json("eb_dblp_2005.json", eb_dblp_2005)
write_json("eb_dblp_2006.json", eb_dblp_2006)
write_json("eb_dblp_2005_w.json", eb_dblp_2005_w)

### Link Prediction in Graphs ###

## i) ##
print("Creating Graph, dblp_2005_core using nodes d >= 3 ...")
dblp_2005_core = nx.Graph(dblp_2005)
rm_2005 = [n for n,d in dict(dblp_2005_core.degree()).items() if d < 3]
dblp_2005_core.remove_nodes_from(rm_2005)
print("Rpeoring ...")
print(report_nodes_edges(dblp_2005_core))

## ii) ##
print("Creating Graph, dblp_2006_core using nodes d >= 3 ...")
dblp_2006_core = nx.Graph(dblp_2006)
rm_2006 = [n for n,d in dict(dblp_2006_core.degree()).items() if d < 3]
dblp_2006_core.remove_nodes_from(rm_2006)
print("Reporting ...")
print(report_nodes_edges(dblp_2006_core))

## iii) ###
print("Generating Firends of Friends, 2 hops away  ...")
s = dict(nx.all_pairs_shortest_path_length(dblp_2005_core, cutoff=2))
fof = list()
j = 0
for key, value in s.items():
    for k, v in value.items():
        if v == 2:
            fof.append({key, k})
print(f"Friends of Friends: {len(fof)}")

## iv) ##
print("Finidng difference of edges between dblp_2006_core and dblp_2005_core")

diff_dblp_2006_2005_core = nx.Graph(dblp_2006_core)
diff_dblp_2006_2005_core.remove_edges_from(dblp_2005_core.edges)
#this is the set of edges for the question
t_edges = diff_dblp_2006_2005_core.edges

print(f"Number of edges in dblp_2005_core: {dblp_2005_core.number_of_edges()}")
print(f"Number of edges in dblp_2006_core: {dblp_2006_core.number_of_edges()}")
print(f"Number of edges in diff_dblp_2006_2005_core: {diff_dblp_2006_2005_core.number_of_edges()}")

## v) ##

## vi) ##

### Community Detection in Graphs ###
















