############################################
# EECS 4414 Infomation Networks
# York University Fall 2021
# Assignment 2
# November 17, 2021
# Hong Chen, hjc@my.yorku.ca
# Christian Augustyn, chrisaug@my.yorku.ca
############################################

import matplotlib.pyplot as plt
from os import read
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.link_prediction import *
import json
import os
import random
import copy

from networkx.classes.function import common_neighbors

path = f"{os.getcwd()}/dblp_coauthorship.json"


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
    sorted_keys = sorted(pr, key=lambda x: x[1], reverse=True)
    for k in sorted_keys:
        sorted_pr[k] = pr[k]

    return sorted_pr


def get_sorted_edge_betweeness(g, weighted):
    if (weighted):
        eb = nx.edge_betweenness_centrality(g, k=100, weight="weight")
    else:
        eb = nx.edge_betweenness_centrality(g, k=100)

    sorted_eb = {}
    sorted_keys = sorted(eb, key=lambda x: x[1], reverse=True)
    for k in sorted_keys:
        sorted_eb[k] = eb[k]

    return sorted_eb


def get_first_N(d, n):
    d_items = d.items()
    return list(d_items)[0:n]


def number_in_target(edges, target):
    in_target = 0
    target = set(target)
    for edge in edges:
        if edge in target or tuple(reversed(edge)) in target:
            in_target += 1
    return (in_target, len(target), in_target / len(target))


print(f"Reading json from: {path}\n")
data = read_json(path)

# ---------------------------------------------------------------------------------------
# Section A
# Temporal Graphs
# ---------------------------------------------------------------------------------------
print("SECTION A----------------------------------------\n")

# ---------------
# A.a) dblp2005
# ---------------
print("A.a) Generating graph dblp_2005 ...")
dblp_2005 = nx.Graph()
for t in data:
    n1, n2, year = t
    if (year == 2005):
        dblp_2005.add_edge(n1, n2)

gcc = get_gcc(dblp_2005)
report = report_nodes_edges(gcc)
print(f"{report}\n")

# ---------------
# A.b) dblp2006
# ---------------
print("A.b) Generating graph dblp_2006 ...")
dblp_2006 = nx.Graph()
for t in data:
    n1, n2, year = t
    if (year == 2006):
        dblp_2006.add_edge(n1, n2)

gcc = get_gcc(dblp_2006)
report = report_nodes_edges(gcc)
print(f"{report}\n")

# ----------------
# A.c) dblp2006w
# ----------------
print("A.c) Generating graph dblp_2005_w ...")
dblp_2005_w = nx.Graph()
for t in data:
    n1, n2, year = t
    if (year == 2005):
        if (dblp_2005_w.has_edge(n1, n2)):
            dblp_2005_w[n1][n2]["weight"] += 1
        else:
            dblp_2005_w.add_edge(n1, n2, weight=1)

gcc = get_gcc(dblp_2005_w)
report = report_nodes_edges(gcc)
print(f"{report}\n")

# ---------------------------------------------------------------------------------------
# Section B
# Node and Edge Importance in Graphs
# ---------------------------------------------------------------------------------------
print("SECTION B----------------------------------------\n\n")

# # ---------------
# # B.i) PageRank
# # ---------------
print("B.i) Getting Page rank importance ...")
pr_dblp_2005 = get_first_N(get_sorted_pagerank(dblp_2005), 50)
pr_dblp_2006 = get_first_N(get_sorted_pagerank(dblp_2006), 50)
pr_dblp_2005_w = get_first_N(get_sorted_pagerank(dblp_2005_w), 50)
print("Writing results ...")
write_json("pr_dblp_2005.json", pr_dblp_2005)
write_json("pr_dblp_2006.json", pr_dblp_2006)
write_json("pr_dblp_2005_w.json", pr_dblp_2005_w)
print("Results written\n")

# # -----------------------
# # B.ii) Edge Betweenness
# # -----------------------
print("B.ii) Getting Edge Betweeness importance ...")
# Probably need top run with k=1000
eb_dblp_2005 = get_first_N(get_sorted_edge_betweeness(dblp_2005, False), 20)
eb_dblp_2006 = get_first_N(get_sorted_edge_betweeness(dblp_2006, False), 20)
eb_dblp_2005_w = get_first_N(get_sorted_edge_betweeness(dblp_2005_w, True), 20)
print("Writing results ...")
write_json("eb_dblp_2005.json", eb_dblp_2005)
write_json("eb_dblp_2006.json", eb_dblp_2006)
write_json("eb_dblp_2005_w.json", eb_dblp_2005_w)
print("Results written\n")

# ---------------------------------------------------------------------------------------
# Section C
# Link Prediction in Graphs
# ---------------------------------------------------------------------------------------
print("SECTION C----------------------------------------\n\n")

# -------------------
# C.i) dbl2005-core
# -------------------
print("C.i) Creating Graph, dblp_2005_core using nodes d >= 3 ...")
dblp_2005_core = nx.Graph(dblp_2005)
rm_2005 = [n for n, d in dict(dblp_2005_core.degree()).items() if d < 3]
dblp_2005_core.remove_nodes_from(rm_2005)
print("Reporting ...")
print(f"{report_nodes_edges(dblp_2005_core)}\n")

# --------------------
# C.ii) dbl2006-core
# --------------------
print("C.ii) Creating Graph, dblp_2006_core using nodes d >= 3 ...")
dblp_2006_core = nx.Graph(dblp_2006)
rm_2006 = [n for n, d in dict(dblp_2006_core.degree()).items() if d < 3]
dblp_2006_core.remove_nodes_from(rm_2006)
print("Reporting ...")
print(f"{report_nodes_edges(dblp_2006_core)}\n\n")

# ----------------------------
# C.iii) FoF in dbl2005-core
# ----------------------------
print("C.iii) Generating Firends of Friends, 2 hops away...")
s = dict(nx.all_pairs_shortest_path_length(dblp_2005_core, cutoff=2))
fof = list()
j = 0
for key, value in s.items():
    for k, v in value.items():
        if v == 2:
            fof.append((key, k))
print(f"Friends of Friends: {len(fof)}\n")

# -----------------------------------------------------
# C.iv) Edges not in dbl2005-core but in dbl2006-core
# -----------------------------------------------------
print("C.iv) Finidng difference of edges between dblp_2006_core and dblp_2005_core")

diff_dblp_2006_2005_core = nx.Graph(dblp_2006_core)
diff_dblp_2006_2005_core.remove_edges_from(dblp_2005_core.edges)
# this is the set of edges for the question
t_edges = diff_dblp_2006_2005_core.edges

print(f"Number of edges in dblp_2005_core: {dblp_2005_core.number_of_edges()}")
print(f"Number of edges in dblp_2006_core: {dblp_2006_core.number_of_edges()}")
print(
    f"Number of edges in diff_dblp_2006_2005_core: {diff_dblp_2006_2005_core.number_of_edges()}\n")

# # ------------------------------
# # C.v) Set of Predictive Edges
# # ------------------------------
print("C.v) Predicting edges using different algorithms...")

rd_predictor_results = copy.deepcopy(fof)
random.shuffle(rd_predictor_results)
print(f"# of candidates with rd: {len(rd_predictor_results)}")

cn_predictor_results = []
for node in fof:
    cn_predictor_results.append(
        (node[0], node[1], len(
            list(common_neighbors(dblp_2005_core, node[0], node[1]))))
    )
cn_predictor_results.sort(key=lambda x: x[2], reverse=True)
print(f"# of candidates with cn: {len(cn_predictor_results)}")

jc_predictor_results = [
    x for x in jaccard_coefficient(dblp_2005_core, ebunch=fof)]
jc_predictor_results.sort(key=lambda x: x[2], reverse=True)
print(f"# of candidates with jc: {len(jc_predictor_results)}")

pa_predictor_results = [
    x for x in preferential_attachment(dblp_2005_core, ebunch=fof)]
pa_predictor_results.sort(key=lambda x: x[2], reverse=True)
print(f"# of candidates with pa: {len(pa_predictor_results)}")

aa_predictor_results = [
    x for x in adamic_adar_index(dblp_2005_core, ebunch=fof)]
aa_predictor_results.sort(key=lambda x: x[2],  reverse=True)
print(f"# of candidates with aa: {len(aa_predictor_results)}")

# ----------------------
# C.vi) Precision at k
# ----------------------
print("C.vi) Calculate precision at k for k={10, 20, 50, 100, |T|}")

k = [10, 20, 50, 100, diff_dblp_2006_2005_core.number_of_edges()]
for top_k in k:
    # for each list of predicted edges, take first k and remove score (except rd)
    # then check how many of them are in target
    print(f"k={top_k}")
    top_k_rd = rd_predictor_results[0:top_k]
    count, total, percent = number_in_target(top_k_rd, t_edges)
    print(f"rd: {{count: {count}, total: {top_k}, percent: {count/top_k}}}")

    top_k_cn = [(a, b) for (a, b, c) in cn_predictor_results[0:top_k]]
    count, total, percent = number_in_target(top_k_cn, t_edges)
    print(f"cn: {{count: {count}, total: {top_k}, percent: {count/top_k}}}")

    top_k_jc = [(a, b) for (a, b, c) in jc_predictor_results[0:top_k]]
    count, total, percent = number_in_target(top_k_jc, t_edges)
    print(f"jc: {{count: {count}, total: {top_k}, percent: {count/top_k}}}")

    top_k_pa = [(a, b) for (a, b, c) in pa_predictor_results[0:top_k]]
    count, total, percent = number_in_target(top_k_pa, t_edges)
    print(f"pa: {{count: {count}, total: {top_k}, percent: {count/top_k}}}")

    top_k_aa = [(a, b) for (a, b, c) in aa_predictor_results[0:top_k]]
    count, total, percent = number_in_target(top_k_aa, t_edges)
    print(f"aa: {{count: {count}, total: {top_k}, percent: {count/top_k}}}")

    print()


# ---------------------------------------------------------------------------------------
# Section D
# Community Detection in Graphs
# ---------------------------------------------------------------------------------------
print("SECTION D----------------------------------------\n\n")


# def community_detection(g):
#     k = 10
#     community_sizes = []
#     print("Applying Girvan-Newman detection ...")
#     com = girvan_newman(g)
#     limit = itertools.takewhile(lambda c: len(c) <= k, com)

#     for commun in limit:
#         for c in commun:
#             community_sizes.append(len(c))

#     return sorted(community_sizes, reverse=True)


# print("Creating smaller dblp_2005_core with d < 4")
# dblp_2005_core_small = nx.Graph(dblp_2005)
# rm_2005_small = [n for n, d in dict(
#     dblp_2005_core_small.degree()).items() if d >= 4]
# dblp_2005_core_small.remove_nodes_from(rm_2005_small)
# print(community_detection(dblp_2005_core_small))
