import os, csv
import pandas as pd
import networkx as nx
from networkx.readwrite import json_graph
from networkx.drawing.nx_pydot import write_dot
from datetime import datetime
from collections import defaultdict, Counter

def get_top_children(g, source, top_n):
    child_list = list(nx.DiGraph.successors(g, source))
    child_weight_dict = {}
    
    for child in child_list:
        child_weight_dict[child] = g[source][child]['weight']
    
    child_weight_dict = {k: v for k, v in sorted(child_weight_dict.items(), 
                        key=lambda item: item[1], reverse = True)}
    return list(child_weight_dict.keys())[:top_n]

def draw_graph(filename, output='output.png', nodes = [], threshold = 0.1,):
    data_df = pd.read_csv(filename)
    g = nx.DiGraph()
    for index, row in data_df.iterrows():
        if row['weight'] > threshold:
            g.add_edge(row['parent'], row['child'], weight = row['weight'])
    
    if len(nodes) > 0:
        sample_g = g.subgraph(nodes)
    else:
        sample_g = g
    draw_sample_g = nx.DiGraph()

    pos = nx.nx_agraph.graphviz_layout(sample_g, prog="dot", args="-Granksep=1")
    for node in list(sample_g.nodes()):
        draw_sample_g.add_node(node, fontcolor = 'blue', font_size = 1000, 
                          pos="%f,%f!" % (pos[node][0], pos[node][1]))

    for node1, node2 in list(sample_g.edges()):
        draw_sample_g.add_edge(node1, node2, penwidth = sample_g[node1][node2]['weight'] * 3)
    
    draw_sample_g.graph['edges']={'arrowsize':'5.0'}
    draw_sample_g.graph['node'] = {'shape':'plaintext', 'margin':0, 'width':0, 'height': 0}
    draw_sample_g.graph['graph'] = {'splines': 'line', "ranksep": 2}

    A =  nx.drawing.nx_agraph.to_agraph(draw_sample_g)
    pos = A.layout('dot')
    A.draw('output.dot')

    os.system("neato -n -Tpng output.dot > {}".format(output))

def get_parent_subs(sub_founders_dic, author_sub_timestamps_dic, directory, days_diff = 7):
    sub_parent_subs_dic = defaultdict(list)
    for sub in sub_founders_dic:
        parent_subs = []
        founders_list = sub_founders_dic[sub]

        for founder, starting_time in founders_list:
            sub_timestamps_list = author_sub_timestamps_dic[founder]
            for p_sub, timestamp in sub_timestamps_list:
                if timestamp >= starting_time:
                    break
                if (datetime.fromtimestamp(starting_time) - datetime.fromtimestamp(timestamp)).days < days_diff:
                    sub_parent_subs_dic[sub].append(p_sub)
      
    filename = "{}parent_child_weights.csv".format(directory)
    f = open(filename, "wt")
    writer = csv.writer(f)
    writer.writerow(['parent', 'child', 'weight'])
    for sub in sub_parent_subs_dic:
        p_subs = sub_parent_subs_dic[sub]
        total = len(p_subs)
        sub_count = Counter(p_subs)
        for p_sub in set(p_subs):
            writer.writerow([p_sub, sub, sub_count[p_sub] / total])
    f.close()
    
    return filename