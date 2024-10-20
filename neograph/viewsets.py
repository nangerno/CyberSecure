from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from neo4j import GraphDatabase
import json
from dj_proj.settings import NEOMODEL_NEO4J_BOLT_URL_API, NEO_NEO4J_AUTH

class SearchByKeywords(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, keywords=None):
        driver = GraphDatabase.driver(NEOMODEL_NEO4J_BOLT_URL_API,auth=NEO_NEO4J_AUTH)
        contains = f'(?i).*{keywords}.*'

        with driver.session() as session:
            q = "MATCH p=(a)-[r]-(b) WHERE a.name =~ $contains RETURN p"
            res = session.run(q, contains=contains)
            data = {'nodes':[{'id':n.element_id,'label':n['name'],'type':n['type']} for n in res.graph().nodes],
                    'links':[dict( {
                        'source':rel.start_node.element_id,
                        'target':rel.end_node.element_id,
                        'relationship_type':vars(rel).get('_properties').get('relationship_type')}) for rel in res.graph().relationships],}
            return Response(data, status=status.HTTP_200_OK)
