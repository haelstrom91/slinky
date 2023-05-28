import yaml

def read_semantics(database):
    with open(f"semantics/{database}.yml", "r") as stream:
        try:
            semantics = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return semantics


def write_yaml(dict, filename):    
    with open(filename,"w") as file:
        yaml.dump(dict, file)
        file.close()