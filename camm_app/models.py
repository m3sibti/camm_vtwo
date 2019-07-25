from django.db import models
from .JSONField import *
import json


# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=200)
    tagline = models.TextField()

    def __str__(self):
        return self.name


# Model for Paper
class Paper(models.Model):
    URL = models.TextField()
    abstract = models.TextField()
    container_title = models.CharField(max_length=150, db_column='container-title', verbose_name='container-title')
    id = models.CharField(max_length=200, primary_key=True)
    keyword = models.TextField()
    page = models.CharField(max_length=20)
    title = models.TextField()
    type = models.CharField(max_length=50)
    volume = models.CharField(max_length=20)
    author_list = models.TextField(default='NONE')
    # two non-String fields
    issued = JSONField(blank=True, null=True)
    author = JSONField(blank=True, null=True)

    def __str__(self):
        return f'Paper {self.id}'

    # @property
    # def issued(self):
    #     x = self.issued['date-parts']
    #     return x

    def keyword_list(self):
        keywords = []
        if self.keyword:
            if ',' in self.keyword:
                keywords = self.keyword.split(',')
            elif ';' in self.keyword:
                keywords = self.keyword.split(';')
        return keywords

    def get_issued(self):
        year = str(self.issued['date-parts'][0]).replace('[', '')
        year = year.replace(']', '')
        # month = self.issued['date-parts'][0][0]
        return f'Issued: {year}'

    def get_author(self):
        family = self.author[0].get('family', 'Anonymous')
        given = (self.author[0].get('given', 'No-one')).replace('(', '').replace(')', '')
        return f'{family}, {given}'

    def get_author_fam(self):
        family = self.author[0].get('family', 'Anonymous')
        return family

    def get_author_given(self):
        given = (self.author[0].get('given', 'No-one')).replace('(', '').replace(')', '')
        return given

    def get_author_list(self):
        m_author_list = []
        if self.author_list:
            if ',' in self.author_list:
                m_author_list = self.author_list.split(',')

        return m_author_list


# Model for Paper 2
class PaperWithRefs(models.Model):
    DOI = models.CharField(max_length=500)
    ISSN = models.CharField(max_length=200)
    container_title = models.CharField(max_length=150, db_column='container-title', verbose_name='container-title')
    id = models.CharField(max_length=200, primary_key=True)
    genre = models.CharField(max_length=20)
    keyword = models.TextField()
    title = models.TextField()
    publisher = models.CharField(max_length=150)
    issue = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    volume = models.CharField(max_length=20)
    # two non-String fields
    issued = JSONField(blank=True, null=True)
    author = JSONField(blank=True, null=True)
    page = models.TextField(default='NONE')

    def __str__(self):
        return f'Paper {self.id}'

    def keyword_list(self):
        keywords = []
        if self.keyword:
            if ',' in self.keyword:
                keywords = self.keyword.split(',')
            elif ';' in self.keyword:
                keywords = self.keyword.split(';')
        return keywords

    def get_issued(self):
        year = str(self.issued['date-parts'][0]).replace('[', '')
        year = year.replace(']', '')
        # month = self.issued['date-parts'][0][0]
        return f'Issued: {year}'

    def get_author(self):
        family = self.author[0].get('family', 'Anonymous')
        given = (self.author[0].get('given', 'No-one')).replace('(', '').replace(')', '')
        return f'{family}, {given}'

    def get_author_fam(self):
        family = self.author[0].get('family', 'Anonymous')
        return family

    def get_author_given(self):
        given = (self.author[0].get('given', 'No-one')).replace('(', '').replace(')', '')
        return given
