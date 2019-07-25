from django.shortcuts import render
from .models import Paper, PaperWithRefs
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from graphviz import Digraph, Graph


class PaperListView(ListView):
    model = Paper
    template_name = 'camm_app/blog.html'
    context_object_name = 'paper'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        author_name = self.request.GET.get('a')
        if query:
            return Paper.objects.filter(title__icontains=query)
        if author_name:
            my_papers = Paper.objects.all()
            new_paper_list = []
            for my_paper in my_papers:
                if author_name.casefold() in my_paper.get_author_fam().casefold():
                    new_paper_list.append(my_paper)
            return new_paper_list
        else:
            return Paper.objects.all()


class PaperListView2(ListView):
    model = Paper
    template_name = 'camm_app/paper_prac.html'
    context_object_name = 'paper'
    paginate_by = 5

    @staticmethod
    def create_mind_map(c_node: Paper, data):
        mm = Digraph(name=f'mind_map{c_node.id}',
                     filename=f'media/mind_maps/mind_map{c_node.id}.gv',
                     strict=True,
                     )
        # TODO check different engines by_default , circo, fdp, neato, patchwork, twopi,

        mm.attr('node', shape='doubleoctagon', color='red')
        mm.node(c_node.title)

        c_node_author = f'Author\n{c_node.get_author_fam()}'
        mm.attr('node', shape='diamond', color='blue')
        mm.node(c_node_author)
        mm.node('Keyword')

        mm.edges([(c_node.title, c_node_author), (c_node.title, 'Keyword'), (c_node.title, 'Co-Authors')])
        current_count = 3

        keywords = c_node.keyword_list()

        mm.attr('node', shape='ellipse', color='yellow')
        for i, kword in enumerate(keywords):
            mm.node(kword)
            mm.edge('Keyword', kword)
            current_count += 1

        author_other_papers = []
        for e_node in data:
            if c_node.get_author_fam().casefold() == e_node.get_author_fam().casefold():
                if c_node.id.casefold() != e_node.id.casefold():
                    author_other_papers.append(e_node)

        if len(author_other_papers):
            mm.attr('node', shape='circle', color='black')
            for ai, a_paper in enumerate(author_other_papers):
                mm.node(a_paper.id)
                mm.edge(c_node_author, a_paper.id)
                current_count += 1

        matched_nodes = []
        for e_node in data:
            for kword2 in keywords:
                if kword2 in e_node.keyword_list():
                    matched_nodes.append(e_node)

        matched_nodes_dict = {}
        for m_node in matched_nodes:
            matched_nodes_dict.update({m_node.id: m_node.keyword_list()})

        matched_nodes_dict.pop(c_node.id)

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

        a_list = c_node.get_author_list()
        # print(a_list)
        mm.attr('node', shape='rectangle', color='purple')
        for a in a_list:
            mm.edge('Co-Authors', a)

        mm.attr('node', shape='octagon', color='blue')
        for aa in a_list:
            for d in data:
                d_title = d.title
                d_list = d.get_author_list()
                for d_aa in d_list:
                    if aa.casefold() == d_aa.casefold():
                        mm.edge(aa, d_title)

        mm.view()

    def go_for_mindmap(self, p_name):
        data = Paper.objects.all()
        my_obj = Paper.objects.filter(title__icontains=p_name)
        self.create_mind_map(my_obj[0], data)

    def get_queryset(self):
        query = self.request.GET.get('q')
        author_name = self.request.GET.get('a')
        btn_clicked = self.request.GET.get('m_btn')
        if btn_clicked:
            data_to_use = self.request.GET.get('m_paper')
            self.request.GET._mutable = True
            self.request.GET.pop('m_paper')
            self.go_for_mindmap(data_to_use)
        if query:
            return Paper.objects.filter(title__icontains=query)
        if author_name:
            my_papers = Paper.objects.all()
            new_paper_list = []
            for my_paper in my_papers:
                if author_name.casefold() in my_paper.get_author_fam().casefold():
                    new_paper_list.append(my_paper)
            return new_paper_list
        else:
            return Paper.objects.all()


class PaperListView3(ListView):
    model = PaperWithRefs
    template_name = 'camm_app/paper_ref_prac.html'
    context_object_name = 'paper'
    paginate_by = 5

    @staticmethod
    def create_mind_map(c_node: Paper, data):
        mm = Digraph(name=f'mind_map{c_node.id}',
                     filename=f'media/mind_maps/mind_map{c_node.id}.gv',
                     strict=True,
                     )
        # TODO check different engines by_default , circo, fdp, neato, patchwork, twopi,

        mm.attr('node', shape='doubleoctagon', color='red')
        mm.node(c_node.title)

        c_node_author = f'Author\n{c_node.get_author_fam()}'
        mm.attr('node', shape='diamond', color='blue')
        mm.node(c_node_author)
        mm.node('Keyword')

        mm.edges([(c_node.title, c_node_author), (c_node.title, 'Keyword')])
        current_count = 3

        keywords = c_node.keyword_list()

        mm.attr('node', shape='ellipse', color='yellow')
        for i, kword in enumerate(keywords):
            mm.node(kword)
            mm.edge('Keyword', kword)
            current_count += 1

        author_other_papers = []
        for e_node in data:
            if c_node.get_author_fam().casefold() == e_node.get_author_fam().casefold():
                if c_node.id.casefold() != e_node.id.casefold():
                    author_other_papers.append(e_node)

        if len(author_other_papers):
            mm.attr('node', shape='circle', color='black')
            for ai, a_paper in enumerate(author_other_papers):
                mm.node(a_paper.id)
                mm.edge(c_node_author, a_paper.id)
                current_count += 1

        matched_nodes = []
        for e_node in data:
            for kword2 in keywords:
                if kword2 in e_node.keyword_list():
                    matched_nodes.append(e_node)

        matched_nodes_dict = {}
        for m_node in matched_nodes:
            matched_nodes_dict.update({m_node.id: m_node.keyword_list()})

        matched_nodes_dict.pop(c_node.id)

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

        mm.view()

    def create_ref_mmap(self, strx):
        mm = Graph(
            name=f'mind_map{strx.id}',
            filename=f'media/mind_maps/mind_map{strx.id}.gv',
            strict=True,
            engine='fdp'
        )
        # print(f'\nTitle {strx.get("title", "A")}')
        # other_nodes(mm, strx)
        cites = strx.page
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
            gri = strx.DOI if strx.DOI else strx.title
            gri = gri[:gri.find(":")]
            mm.edge(gri, k)
            # print(f'- {k}')

        # print('\n')
        mm.view()

    def go_for_mindmap(self, p_id):
        my_obj = PaperWithRefs.objects.filter(id__contains=p_id)
        if my_obj:
            print(f'\n\n\n\n{my_obj}\n\n\n\n')
            self.create_ref_mmap(my_obj[0])

    def get_queryset(self):
        query = self.request.GET.get('q')
        author_name = self.request.GET.get('a')
        btn_clicked = self.request.GET.get('m_btn')
        if btn_clicked:
            data_to_use = self.request.GET.get('m_paper')
            # self.request.GET._mutable = True
            # self.request.GET.pop('m_paper')
            self.go_for_mindmap(data_to_use)
        if query:
            return PaperWithRefs.objects.filter(title__icontains=query)
        if author_name:
            my_papers = PaperWithRefs.objects.all()
            new_paper_list = []
            for my_paper in my_papers:
                if author_name.casefold() in my_paper.get_author_fam().casefold():
                    new_paper_list.append(my_paper)
            return new_paper_list
        else:
            return sorted(PaperWithRefs.objects.all(), key=lambda o: len(getattr(o, 'page')), reverse=True)


# TODO Enable this so only register users can see papers @login_required
def all_papers(req):
    if req.method == 'POST':
        print('Hello buddy')
    papers = Paper.objects.all()
    content = {'paper': papers}
    return render(req, 'camm_app/blog.html', content)


def about_view(req):
    return render(req, 'camm_app/about.html')
