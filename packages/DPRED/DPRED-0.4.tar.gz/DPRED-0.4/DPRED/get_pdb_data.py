import requests

class GetPDB:
    def __init__(self, pfam: str, l: list, res: int, mut: int, iden: int) -> None:
        self.pfam, self.l, self.res, self.mut, self.iden = pfam, l, res, mut, iden
        self.dir_name, self.j = 'input_pdb/', self._req()
    
    def _req(self) -> dict:
        '''A function to get a representative set of pdb ids with chains'''
    
        # Returned as: Polymer entities  
        # Displaying as = Representatives
        
        api_query = '''
        {
            "query": {
                "type": "group",
                "logical_operator": "and",
                "nodes": [
                {
                    "type": "group",
                    "logical_operator": "and",
                    "nodes": [
                    {
                        "type": "terminal",
                        "service": "text",
                        "parameters": {
                            "attribute": "rcsb_polymer_entity_annotation.annotation_id",
                            "operator": "exact_match",
                            "negation": false,
                            "value": "%s"
                        }
                    },
                    {
                        "type": "terminal",
                        "service": "text",
                        "parameters": {
                            "attribute": "rcsb_polymer_entity_annotation.type",
                            "operator": "exact_match",
                            "value": "Pfam",
                            "negation": false
                        }
                    }
                    ],
                "label": "nested-attribute"
            },
        {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_entry_info.diffrn_resolution_high.value",
                "operator": "less_or_equal",
                "negation": false,
                "value": %s
            }
        },
        {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "entity_poly.rcsb_sample_sequence_length",
                "operator": "range",
                "negation": false,
                "value": {
                    "from": %s,
                    "to": %s,
                    "include_lower": true,
                    "include_upper": true
                }
            }
        },
        {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "entity_poly.rcsb_mutation_count",
                "operator": "equals",
                "negation": false,
                "value": %s
            }
        }
        ],
        "label": "text"
        },
        "return_type": "polymer_entity",
        "request_options": {
            "group_by_return_type": "representatives",
            "group_by": {
                "aggregation_method": "sequence_identity",
                "ranking_criteria_type": {
                    "sort_by": "rcsb_entry_info.resolution_combined",
                    "direction": "asc"
                },
                "similarity_cutoff": %s
            },
            "paginate": {
                "start": 0,
                "rows": 25
            },
            "results_content_type": [
                "experimental"
            ],
            "sort": [
            {
                "sort_by": "score",
                "direction": "desc"
            }
            ],
            "scoring_strategy": "combined"
            }
        }''' % (self.pfam, self.res, int(self.l[0]), int(self.l[1]), self.mut, self.iden)
        
        r1 = requests.get(f'http://search.rcsb.org/rcsbsearch/v2/query?json={requests.utils.requote_uri(api_query)}')
        j1 = r1.json()
        ids = [dict['identifier'] for dict in j1['result_set']]
        
        graphiql_query = '''
        {
            polymer_entities(entity_ids: %s)
            {
                rcsb_id
                entity_poly {
                    pdbx_seq_one_letter_code_can
                }
                polymer_entity_instances {
                    rcsb_polymer_entity_instance_container_identifiers {
                        auth_asym_id
                    }
                }
            }
        }''' % str(ids).replace("'", '"')
        
        r2 = requests.get(f'https://data.rcsb.org/graphql?query={requests.utils.requote_uri(graphiql_query)}')
        return r2.json()

    def get_ids(self) -> str:
        ids = ''
        for dict in self.j['data']['polymer_entities']:
            id = dict['rcsb_id'][:4].lower()
            chain = dict['polymer_entity_instances'][0]['rcsb_polymer_entity_instance_container_identifiers']['auth_asym_id']
            ids += id + chain + "\n"
        return ids
            
    def get_fasta(self) -> str:
        fasta = ''
        for dict in self.j['data']['polymer_entities']:
            id = dict['rcsb_id'][:4].lower()
            chain = dict['polymer_entity_instances'][0]['rcsb_polymer_entity_instance_container_identifiers']['auth_asym_id']
            seq = dict['entity_poly']['pdbx_seq_one_letter_code_can']
            fasta += ">" + id + ":" + chain + "\n" + seq + "\n"
        return fasta.rstrip()
        
    def get_lst(self) -> str:
        lst = ''
        for dict in self.j['data']['polymer_entities']:
            id = dict['rcsb_id'][:4].lower()
            chain = dict['polymer_entity_instances'][0]['rcsb_polymer_entity_instance_container_identifiers']['auth_asym_id']
            lst += self.dir_name + "pdb" + id + "_" + chain + ".pdb\n"
        return lst