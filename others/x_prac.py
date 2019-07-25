import json
from graphviz import Digraph, Graph

with open('savedrecs_cc.json', 'r') as f:
    data = json.load(f)

    mm = Graph(name=f'mind_map0',
               filename=f'x_test_out/mind_map0.gv',
               strict=True,
               engine='fdp')

firstElement = data[0]
# print(firstElement)

# for k in data:
#     print(k)

keys = []
for x in firstElement:
    keys.append(x)


def get_author_fam_no_case(node):
    family = node['author'][0].get('family', 'Anonymous').casefold()
    return family


def get_keywords(my_node):
    keywords = []
    if ',' in my_node.get('keyword', 'NONE'):
        keywords = my_node['keyword'].split(',')
    elif ';' in my_node.get('keyword', 'NONE'):
        keywords = my_node['keyword'].split(';')
    return keywords


def other_nodes(mm, strx):
    mm.attr('node', shape='doubleoctagon', color='red')
    mm.node(strx['title'])

    c_node_author = f'Author\n{strx["author"][0]["family"]}'
    mm.attr('node', shape='diamond', color='blue')
    mm.node(c_node_author)
    mm.node('Keyword')

    mm.edges([(strx['title'], c_node_author), (strx['title'], 'Keyword')])
    current_count = 3

    keywords = []
    if ',' in strx.get('keyword', 'NONE'):
        keywords = strx['keyword'].split(',')
    elif ';' in strx.get('keyword', 'NONE'):
        keywords = strx['keyword'].split(';')
    else:
        pass

    # print(keywords)
    mm.attr('node', shape='ellipse', color='yellow')
    for i, kword in enumerate(keywords):
        mm.node(kword)
        mm.edge('Keyword', f'{kword}')
        current_count += 1

    author_other_papers = []
    for e_node in data:
        if get_author_fam_no_case(strx) == get_author_fam_no_case(e_node):
            if strx['id'] != e_node['id']:
                author_other_papers.append(e_node)

    if len(author_other_papers):
        mm.attr('node', shape='circle', color='black')
        for ai, a_paper in enumerate(author_other_papers):
            mm.node(a_paper['id'])
            mm.edge(c_node_author, a_paper['id'])
            current_count += 1

    # ----------------Above Code Deployed---------------------- #

    matched_nodes = []
    for e_node in data:
        for kword2 in keywords:
            if kword2 in e_node.get('keyword', 'NONE'):
                matched_nodes.append(e_node)

    matched_nodes_dict = {}
    for m_node in matched_nodes:
        matched_nodes_dict.update({m_node['id']: get_keywords(m_node)})

    # matched_nodes_dict.pop(strx['id'])

    if len(matched_nodes_dict):
        with mm.subgraph(name='cluster_0') as c:
            c.attr('node', shape='circle', color='lightblue')
            c.node_attr.update(style='filled')
            c.attr(label='Other Papers')
            c.attr(color='cyan')
            for i, (page_id, page_kes) in enumerate(matched_nodes_dict.items()):
                c.node(f'{page_id}')
                current_count += 1

    for kword3 in keywords:
        for paper_id, paper_kwords in matched_nodes_dict.items():
            for p_k_word in paper_kwords:
                if kword3 in p_k_word:
                    mm.edge(kword3, paper_id)


# for key in keys:
#     print(f' {key}, type = {type(firstElement[key])}')

def get_references(strx):
    # print(f'\nTitle {strx.get("title", "A")}')
    # other_nodes(mm, strx)
    cites = strx.get('page', 'NONE')
    mlist = cites.split('DOI ')
    mnew_list = []
    for x in mlist:
        # print(x)
        # print('--')
        x = x[:x.find(" ")]
        xt = x[:x.find(":")]
        # xy = xt[:xt.find("::")]
        mnew_list.append(xt)

    for k in mnew_list:
        gri = strx.get('DOI', 'A')
        gri = gri[:gri.find(":")]
        mm.edge(gri, k)
        # print(f'- {k}')

    # print('\n')
    # mm.view()


for i, d in enumerate(data):
    mm = Graph(name=f'mind_map{i}',
               filename=f'x_test_out/mind_map{i}.gv',
               strict=True,
               engine='fdp')
    get_references(d)

# mm.view()

string_keys_elements = []
string_keys = []
nonstring_keys_elements = []
nonstring_keys = []

for key in keys:
    if type(firstElement[key]) == str:
        string_keys.append(key)
        string_keys_elements.append(firstElement[key])
    else:
        nonstring_keys.append(key)
        nonstring_keys_elements.append(firstElement[key])

# print("String Keys: ")
# print(string_keys)
# print("----")
# print("Non- String Keys: ")
# print(nonstring_keys)
# print("----")

for n_str_key in nonstring_keys:
    pass
# print(type(firstElement[n_str_key]))
# print(firstElement[n_str_key])

# print('\nDictionary Fetched: ')
# print(firstElement['issued']['date-parts'][0][0])
# print(firstElement['issued']['date-parts'][0][1])

# print('\n List Fetched: ')
# convertedStr = str(firstElement['author'])
# print(list(convertedStr))
# print(firstElement['author'][0])

# keywords = firstElement['keyword'].split(',')
# print(keywords)
