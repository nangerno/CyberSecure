from django.db.models import Model, TextChoices, CharField, URLField
from django_neomodel import DjangoNode
from neomodel import StringProperty, StructuredRel, ArrayProperty, RelationshipFrom, RelationshipTo
from taxii2client.v20 import Server as Taxii2Ser
from stix2 import TAXIICollectionSource
import json

class RelManager():
    def __init__(self, **kwargs):
        source_type = kwargs['source_ref'].split('--')[0]
        target_type = kwargs['target_ref'].split('--')[0]
        try:
            source_obj_type = MAP_OBJ[source_type]
            target_obj_type = MAP_OBJ[target_type]
            source_obj = source_obj_type.nodes.get_or_none(stix_id=kwargs['source_ref'])
            target_obj = target_obj_type.nodes.get_or_none(stix_id=kwargs['target_ref'])

            if source_obj and target_obj:
                rel_attr = target_type.replace('-','_')
                rel = None
                try:
                    rel = getattr(source_obj,rel_attr).relationship(target_obj)
                except Exception as e:
                    pass
                if rel is None:
                    getattr(source_obj, rel_attr).connect(target_obj,kwargs)
        except Exception as e:
                pass

class StixObject(DjangoNode):
    __abstract_node__ = None
    stix_id = StringProperty(required=True)
    type = StringProperty(required=True)
    created = StringProperty(required=True)
    modified = StringProperty(required=True)
    labels = ArrayProperty(StringProperty(), required=False)

    class Meta:
        app_label = 'neograph'


class StixRelationship(StructuredRel):
    __abstract_node__=True
    type = StringProperty(required=True)
    created = StringProperty(required=True)
    modified = StringProperty(required=True)
    labels = ArrayProperty(StringProperty(),required=False)
    relationship_type = StringProperty(required=True)
    source_ref = StringProperty(required=True)
    target_ref = StringProperty(required=True)

class Relationship(StixRelationship):
    description = StringProperty(required=False)


class AttackPattern(StixObject):
    type = StringProperty(default='attack-pattern')
    name = StringProperty(required=True)
    description = StringProperty(required=False)
    external_id = StringProperty(required=False)

    identity = RelationshipTo('Identity', 'targets', model=Relationship)
    attack_pattern = RelationshipTo('AttackPattern', 'subtechnique-of', model=Relationship)
    malware = RelationshipTo('Malware', 'uses', model=Relationship)
    tool = RelationshipTo('Tool', 'uses', model=Relationship)

class Malware(StixObject):
    type = StringProperty(default='malware')
    name = StringProperty(required=True)
    description = StringProperty(required=False)

    # relationships
    attack_pattern = RelationshipTo('AttackPattern', 'uses', model=Relationship)


class Tactic(StixObject):
    type = StringProperty(default='x-mitre-tactic')
    name = StringProperty(required=True)
    description = StringProperty(required=True)
    technique = RelationshipTo('AttackPattern', 'includes', model=Relationship)

class Identity(StixObject):
    type = StringProperty(default='identity')
    name = StringProperty(required=True)
    description = StringProperty(required=False)

    attack_pattern = RelationshipFrom('AttackPattern', 'targets', model=Relationship)

class Campaign(StixObject):
    type = StringProperty(default='campaign')
    name = StringProperty(required=True)
    description = StringProperty(required=False)
    objective = StringProperty(required=False)

    attack_pattern = RelationshipTo('AttackPattern', 'uses', model=Relationship)
    intrusion_set = RelationshipTo('IntrusionSet', 'attribute-to', model=Relationship)
    malware = RelationshipTo('Malware', 'uses', model=Relationship)
    tool = RelationshipTo('Tool', 'uses', model=Relationship)


class CourseOfAction(StixObject):
    type = StringProperty(default='course-of-action')
    name = StringProperty(required=True)
    description = StringProperty(required=False)
    action = StringProperty(required=False)

    attack_pattern = RelationshipTo('AttackPattern', 'mitigates', model=Relationship)
    malware = RelationshipTo('Malware', 'mitigates', model=Relationship)
    tool = RelationshipTo('Tool', 'mitigates', model=Relationship)


class IntrusionSet(StixObject):
    type = StringProperty(default='intrusion-set')
    name = StringProperty(required=True)
    description = StringProperty(required=False)
    action = StringProperty(required=False)
    first_seen = StringProperty(required=False)
    last_seen = StringProperty(required=False)

    attack_pattern = RelationshipTo('AttackPattern', 'uses', model=Relationship)
    malware = RelationshipTo('Malware', 'uses', model=Relationship)
    tool = RelationshipTo('Tool', 'uses', model=Relationship)
  
class Tool(StixObject):
    type = StringProperty(default='tool')
    name = StringProperty(required=True)
    description = StringProperty(required=False)

    attack_pattern = RelationshipTo('AttackPattern', 'uses', model=Relationship)
    malware = RelationshipTo('Malware', 'targets', model=Relationship)
    campaign = RelationshipTo('Campaign', 'uses', model=Relationship)
    intrusion_set = RelationshipTo('IntrusionSet', 'uses', model=Relationship)

class DataSource(StixObject):
    type = StringProperty(default='x-mitre-data-source')
    name = StringProperty(required=True)
    description = StringProperty(required=False)

class DataComponent(StixObject):
    type = StringProperty(default='x-mitre-data-component')
    name = StringProperty(required=True)
    description = StringProperty(required=False)

    attack_pattern = RelationshipTo('AttackPattern', 'detects', model=Relationship)

def update_tactic_technique_relationship():
    '''to do: use data from  attack_pattern--- "kill_chain_phases":     
      [
        {
          "kill_chain_name": "mitre-attack",
          "phase_name": "defense-evasion"
        },
        {
          "kill_chain_name": "mitre-attack",
          "phase_name": "privilege-escalation"
        }
      ],
      
    '''    
    pass 

MAP_OBJ = {
        'attack-pattern':AttackPattern,
        'campaign':Campaign,
        'course-of-action':CourseOfAction,
        'intrusion-set':IntrusionSet,
        'malware':Malware,
        'tool':Tool,
        'x-mitre-data-source':DataSource,
        'x-mitre-data-component':DataComponent,
        'identity':Identity,
        'relationship':RelManager,
        'x-mitre-tactic': Tactic,
    }

class Server(Model):
     
    class Status(TextChoices):
        DONE ='DN'
        NOT_DONE = 'ND'

    url = URLField()
    status = CharField(max_length=2,choices=Status.choices,default=Status.NOT_DONE)

    def __str__(self):
        return self.url
    
    def _get_or_update_obj(self,object):
        if type(object) != dict:
            properties = json.loads(object.serialize())
        else:
            properties = object

        properties['stix_id'] = properties.pop('id','identity')
        if properties['type'] in MAP_OBJ.keys():
            obj_class = MAP_OBJ[properties['type']]

            if obj_class is RelManager:
                RelManager(**properties)
            else:
                obj = obj_class.nodes.get_or_none(stix_id=properties['stix_id'])
                if obj:
                    if properties.get('modified'):
                        new = properties.get('modified')
                        old = obj.modified
                        if new != old:
                            fields = obj._meta.get_fields()
                            for i in fields:
                                if i.name in properties:
                                    obj.__setattr__(i.name,properties[i.name])
                            obj.save()
                else:
                    new_obj = obj_class(**properties)
                    new_obj.save()

class MitreServer(Server):
    description = StringProperty(required=False)

    def update_data(self):
        print(f'taxii server = {self.url}')
        server = Taxii2Ser(self.url) 
        for api_root in server.api_roots:
            print(f'object = ...{api_root}')
            for item in api_root.collections:
                taxii_col = TAXIICollectionSource(item)

                rel =[]
                for obj in taxii_col.query():
                    if not isinstance(obj,dict) and obj.type == 'relationship':
                        rel.append(obj)
                    else:
                        if not isinstance(obj,dict) and hasattr(obj,'revoked') and obj.revoked:
                            pass
                        else:
                            try:
                                self._get_or_update_obj(obj)
                            except Exception as e:
                                print(f'{e}, for object {obj}')
                for obj in rel:
                    self._get_or_update_obj(obj)
        self.save()


