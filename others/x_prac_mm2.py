import json
from graphviz import Digraph

# with open('bibDbJSON.json', 'r') as f:
with open('db_w_author.json', 'r') as f:
    data = json.load(f)

dot = Digraph(comment='Good Graph')


def get_author_fam_no_case(node):
    family = node['author'][0].get('family', 'Anonymous').casefold()
    return family


def get_keywords(my_node):
    keywords = []
    if ',' in my_node.get('keyword', 'NONE'):
        keywords = my_node.get('keyword', 'NONE').split(',')
    elif ';' in my_node.get('keyword', 'NONE'):
        keywords = my_node.get('keyword', 'NONE').split(';')
    return keywords


def get_authorlist(my_node):
    authorList = []
    if ',' in my_node['author_list']:
        authorList = my_node['author_list'].split(',')

    return authorList


def print_dict(mydict):
    for x, y in mydict.items():
        print(f'{x} : {y}')


def create_mind_map(node_num=0):
    my_node = data[node_num]
    mm = Digraph(name=f'mind_map{node_num}', filename=f'x_test_out/mind_map{node_num}.gv', engine='circo')
    # TODO check different engines by_default , circo, fdp, neato, patchwork, twopi,

    mm.attr('node', shape='doubleoctagon', color='red')
    mm.node('0', my_node['title'])

    mm.attr('node', shape='diamond', color='blue')
    mm.node('1', f'Author\n{my_node["author"][0]["family"]}')
    mm.node('2', 'Keyword')

    mm.edges([('0', '1'), ('0', '2')])
    current_count = 3

    keywords = []
    if ',' in my_node.get('keyword', 'NONE'):
        keywords = my_node.get('keyword', 'NONE').split(',')
    elif ';' in my_node.get('keyword', 'NONE'):
        keywords = my_node.get('keyword', 'NONE').split(';')
    else:
        pass

    # print(keywords)
    mm.attr('node', shape='ellipse', color='yellow')
    for i, kword in enumerate(keywords):
        mm.node(f'{i + 3}', kword)
        mm.edge('2', f'{i + 3}')
        current_count += 1

    author_other_papers = []
    for e_node in data:
        if get_author_fam_no_case(my_node) == get_author_fam_no_case(e_node):
            if my_node['id'] != e_node['id']:
                author_other_papers.append(e_node)

    if len(author_other_papers):
        mm.attr('node', shape='circle', color='black')
        for ai, a_paper in enumerate(author_other_papers):
            mm.node(f'{ai + current_count}', a_paper['id'])
            mm.edge('1', f'{ai + current_count}')
            current_count += 1

    # ----------------Above Code Deployed---------------------- #

    matched_nodes = []
    for e_node in data:
        for kword2 in keywords:
            if kword2 in e_node.get('keyword', 'NONE'):
                matched_nodes.append(e_node)

    # print(len(matched_nodes))
    # print(len(matched_nodes))

    matched_nodes_dict = {}
    for m_node in matched_nodes:
        matched_nodes_dict.update({m_node['id']: get_keywords(m_node)})

    matched_nodes_dict.pop(my_node['id'])

    # print_dict(matched_nodes_dict)
    # print(current_count)
    if len(matched_nodes_dict):
        mm.attr('node', shape='rect', color='magenta')
        for i, (page_id, page_kes) in enumerate(matched_nodes_dict.items()):
            mm.node(f'{i + current_count}', f'{page_id}')
            current_count += 1

    for kword3 in keywords:
        mm.edge('4', list(matched_nodes_dict.keys())[0])

    # print(current_count)
    mm.view()


def create_mind_map2(node_num=0):
    my_node = data[node_num]
    mm = Digraph(name=f'mind_map{node_num}',
                 filename=f'x_test_out/mind_map{node_num}.gv',
                 strict=True,
                 engine='circo')
    # mm.attr(size='6,6')
    # TODO check different engines by_default , circo, fdp, neato, patchwork, twopi,

    mm.attr('node', shape='doubleoctagon', color='red')
    mm.node(my_node['title'])

    c_node_author = f'Author\n{my_node["author"][0]["family"]}'
    mm.node(c_node_author)
    mm.node('Keyword')

    mm.edges([(my_node['title'], c_node_author), (my_node['title'], 'Keyword')])
    current_count = 3

    keywords = []
    if ',' in my_node.get('keyword', 'NONE'):
        keywords = my_node.get('keyword', 'NONE').split(',')
    elif ';' in my_node.get('keyword', 'NONE'):
        keywords = my_node.get('keyword', 'NONE').split(';')
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
        if get_author_fam_no_case(my_node) == get_author_fam_no_case(e_node):
            if my_node['id'] != e_node['id']:
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

    # matched_nodes_dict.pop(my_node['id'])

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

    # ------------------ Author Code ----------------------------
    a_list = get_authorlist(my_node)
    print(a_list)
    mm.edge(my_node['title'], 'Authors')
    for a in a_list:
        mm.edge('Authors', a)

    # print(current_count)
    mm.view()


def graph_example():
    u = Digraph('unix', filename='x_test_out/unix.gv')
    u.attr(size='6,6')
    u.node_attr.update(color='lightblue2', style='filled')

    u.edge('5th Edition', '6th Edition')
    u.edge('5th Edition', 'PWB 1.0')
    u.edge('6th Edition', 'LSX')
    u.edge('6th Edition', '1 BSD')
    u.edge('6th Edition', 'Mini Unix')
    u.edge('6th Edition', 'Wollongong')
    u.edge('6th Edition', 'Interdata')
    u.edge('Interdata', 'Unix/TS 3.0')
    u.edge('Interdata', 'PWB 2.0')
    u.edge('Interdata', '7th Edition')
    u.edge('7th Edition', '8th Edition')
    u.edge('7th Edition', '32V')
    u.edge('7th Edition', 'V7M')
    u.edge('7th Edition', 'Ultrix-11')
    u.edge('7th Edition', 'Xenix')
    u.edge('7th Edition', 'UniPlus+')
    u.edge('V7M', 'Ultrix-11')
    u.edge('8th Edition', '9th Edition')
    u.edge('1 BSD', '2 BSD')
    u.edge('2 BSD', '2.8 BSD')
    u.edge('2.8 BSD', 'Ultrix-11')
    u.edge('2.8 BSD', '2.9 BSD')
    u.edge('32V', '3 BSD')
    u.edge('3 BSD', '4 BSD')
    u.edge('4 BSD', '4.1 BSD')
    u.edge('4.1 BSD', '4.2 BSD')
    u.edge('4.1 BSD', '2.8 BSD')
    u.edge('4.1 BSD', '8th Edition')
    u.edge('4.2 BSD', '4.3 BSD')
    u.edge('4.2 BSD', 'Ultrix-32')
    u.edge('PWB 1.0', 'PWB 1.2')
    u.edge('PWB 1.0', 'USG 1.0')
    u.edge('PWB 1.2', 'PWB 2.0')
    u.edge('USG 1.0', 'CB Unix 1')
    u.edge('USG 1.0', 'USG 2.0')
    u.edge('CB Unix 1', 'CB Unix 2')
    u.edge('CB Unix 2', 'CB Unix 3')
    u.edge('CB Unix 3', 'Unix/TS++')
    u.edge('CB Unix 3', 'PDP-11 Sys V')
    u.edge('USG 2.0', 'USG 3.0')
    u.edge('USG 3.0', 'Unix/TS 3.0')
    u.edge('PWB 2.0', 'Unix/TS 3.0')
    u.edge('Unix/TS 1.0', 'Unix/TS 3.0')
    u.edge('Unix/TS 3.0', 'TS 4.0')
    u.edge('Unix/TS++', 'TS 4.0')
    u.edge('CB Unix 3', 'TS 4.0')
    u.edge('TS 4.0', 'System V.0')
    u.edge('System V.0', 'System V.2')
    u.edge('System V.2', 'System V.3')

    u.view()


for i in range(115, 122):
    print(f"\n{i}")
    create_mind_map2(node_num=i)
