import xml.etree.ElementTree as et
import pysolr, json, os

from src.step1.ncbo.ncbo_annotator import Annotator

SOLR_URL = 'http://' + os.environ['SOLR_HOST'] + ':8983/solr/pmc'

class Searcher:

    # def __init__(self):

    def get_query_from_mesh_terms(self, mesh_terms):
        query_search = ''

        for mesh_term in mesh_terms:
            aux = mesh_term.split()
            compound_term = ''
            if len(aux) > 1:
                compound_term = '('

                for x in aux:
                    compound_term = compound_term + '+' + x + ' '
                compound_term = compound_term + ')'
                query_search = query_search + compound_term + ' '
            else:
                query_search = query_search + mesh_term + ' '
        return query_search


    def search_by_category(self, description, filter, mode):
        if mode == 'textword':
            search_query = description
        else:
            a = Annotator()

            mesh_terms = a.get_mesh_terms(description)
            search_query = self.get_query_from_mesh_terms(mesh_terms)

        solr = pysolr.Solr(SOLR_URL)
        query = 'abstract:' + search_query
        return solr.search(q=query, fq=filter)

