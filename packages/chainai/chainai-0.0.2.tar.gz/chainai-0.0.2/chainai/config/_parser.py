import yaml

from chainai._schema import Pipeline
from chainai._utils.graph import cyclic

from pydantic import ValidationError

def read_pipeline_config(yaml_path):
    """Reads the Pipeline definition file at `yaml_path` and returns the Pipeline object.
    :param yaml_path: file path to the Pipeline defintion file.
    :throws pydantic_core._pydantic_core.ValidationError if schema constraints are violated.
    :throws ValueError if uniqueness constraints are violated.
    """
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return parse_pipeline_config(data)

def parse_pipeline_config(data, return_graph = False):
    pipeline = Pipeline(**data)
    config = pipeline.model_dump()
    graph = {}
    for stage in config['stages']:
        graph[stage['id']] = [x['destination'] for x in stage['outputs']]
    if cyclic(graph):
        raise ValidationError.from_exception_data("Pipeline stages create a cycle!")
    ids_seen = set()
    for stage in config['stages']:
        if stage['id'] in ids_seen:
            raise ValueError(f"Duplicate ID {stage['id']} found!")
        ids_seen.add(stage['id'])
        if 'outputs' in stage:
            for output in stage['outputs']:
                if output['id'] in ids_seen:
                    raise ValueError(f"Duplicate ID {stage['id']} found!")
                ids_seen.add(output['id'])
    for stage in config['stages']:
        if 'triggers' in stage:
            for trigger in stage['triggers']:
                if trigger['name'] in ids_seen:
                    raise ValueError(f"Duplicate trigger {trigger['name']} found (or the trigger shares the same name as an ID field)!")
                ids_seen.add(trigger['name'])
    if return_graph:
        return pipeline, graph
    return pipeline