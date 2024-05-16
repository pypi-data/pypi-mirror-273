import sys, os, json, ast
import astunparse
from pathlib import Path
from . import __version_name__
from cookiecutter.main import cookiecutter
from jsonmerge import merge
from cookiecutter.exceptions import OutputDirExistsException


def main():
    if len(sys.argv) > 2:
        print("Invalid command options. Expects 1 argument, found " + str(len(sys.argv)-1))
        return
    elif len(sys.argv) == 1:
        print("expects 1 option ('The integration name'), 0 given")
        return
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-V':
            print(__version_name__)
            pass
        else :
            run_cookiecutter()
    else:
        print("Invalid Command Option")

def run_cookiecutter():
    path = Path(__file__).absolute().parent.parent.joinpath('template').as_posix()
    # print(path)
    name = sys.argv[1]
    id = name.replace(" ", "_")
    classname = name.title().replace(" ","")
    try :
        cookiecutter(path, no_input=True, default_config={}, extra_context={"integration_name":name, "id": id, "classname": classname})
        print("Integration for '" + name + "' created successfully.")
    except OutputDirExistsException as odee:
        print("Error: Integration with name '" + name + "' already exists.")

def reload():
    print("Reloading...")
    path = Path(__file__).cwd().as_posix()
    metaPath = Path(path + "/integration_meta.json") 
    defPath = Path(path + "/integration_definition.json")
    schemaPath = Path(path + "/integration_meta_schema.json")
    classFilePath = os.path.join(path, "app", Path(__file__).cwd().name + '.py')
    className = Path(__file__).cwd().name.title().replace('_', '')
    if not (metaPath.exists() and defPath.exists() and schemaPath.exists() and Path(classFilePath).exists() ) :
        print("Could not find reload meta, Make sure you are pointing to root of integration path")
    else :
        try:
            meta = open(os.path.join(path, "integration_meta.json")).read()
            definition = open(os.path.join(path, "integration_definition.json")).read()
            info_json = merge(json.loads(meta), json.loads(definition))
            functions = info_json['functions']
            functions = [fn['name'] for fn in functions]
            functions.append('__init__')

            code_tree = ast.parse(open(classFilePath, "r").read())
            clazz = next(itm for itm in code_tree.body if isinstance(itm, ast.ClassDef) and itm.name == className)
            code_functions = clazz.body
            code_fun_names = [fn.name for fn in code_functions]
            new_code_functions = []

            # removes the function if its not available in json
            for fnDef in code_functions:
                if fnDef.name in functions:
                    new_code_functions.append(fnDef)

            # adds new function in class if not available
            for fn in info_json['functions']:
                if fn['name'] not in code_fun_names:
                    new_code_functions.append(getFunctionDef(fn, info_json['connectionParameters']))
            
            new_code_functions.append(getTestConnectionFunction(info_json['connectionParameters']))
            clazz.body = new_code_functions
            code = astunparse.unparse(code_tree)
            with open(classFilePath, "w") as code_file:
                code_file.write(code)
            reloadTestScript(path, new_code_functions, info_json)
        except Exception as e:
            print(e)
            raise e
        pass
    print("Reloaded.")

def getTestConnectionFunction(con_params):
    code = "def test_connection(self, connectionParameters: dict):\n"
    for cp in con_params:
        code += '\t' + cp['name'] + ' = connectionParameters[\'' + cp['name'] + '\']\n'
    code += '\ttry:\n'
    code += '\t\treturn "Connection Successful"\n'
    code += '\texcept Exception as e:\n'
    code += '\t\traise Exception(str(e))\n'
    return ast.parse(code).body[0]


def reloadTestScript(path, functions, info_json):
    testClassFilePath = os.path.join(path, "tests", 'test_' + Path(__file__).cwd().name + '.py')
    try:
        code_tree = ast.parse(open(testClassFilePath, "r").read())
        code_functions = []
        for item in code_tree.body:
            if isinstance(item, ast.FunctionDef) :
                code_functions.append(item.name)

        for fn in functions:
            if 'test_' + fn.name not in code_functions and fn.name not in ['__init__','test_connection']:
                code_tree.body.append(getTestFunction(fn.name, info_json))
        code = astunparse.unparse(code_tree)
        with open(testClassFilePath, "w") as code_file:
            code_file.write(code)
    except Exception as e:
        print(e)
        raise e
    pass


def getTestFunction(fn_name, info_json):
    con_params = info_json['connectionParameters']
    params = next(fn for fn in info_json['functions'] if fn['name'] == fn_name)['inParameters']
    req = {'connectionParameters':{},'parameters':{}}
    for cp in con_params:
        req['connectionParameters'][cp['name']] = 'samplevalue'
    for p in params:
        req['parameters'][p['name']] = 'samplevalue'

    code = 'def test_' + fn_name + '():\n'
    code += '\treq = \'' + json.dumps(req) + '\'\n'
    code += '\treq = pykson.from_json(req, RequestBody, True)\n'
    code += '\tresp = integration_class.' + fn_name + '(req)\n'
    code += '\tassert resp is not None\n'
    return ast.parse(code).body[0]


def getFunctionDef(fn, conParams):
    code = 'def ' + fn['name'] + '(self, request: RequestBody) -> ResponseBody:\n'
    # extract connection parameters
    for param in conParams:
        code = code + '\t' + param['name'] + ' = request.connectionParameters[\'' + param['name'] + '\']\n'
    # extract action parameters
    for param in fn['inParameters']:
        code = code + '\t' + param['name'] + ' = request.parameters[\'' + param['name'] + '\']\n'
    code = code + "\t'''implement your custom logic for action handling here'''\n"
    # return dict object with out parameters
    code = code + '\n\treturn {'
    for param in fn['outParameters']:
        code = code + '\t\t"' + param['name'] + '" : "",\n'
    code = code[:-1]
    code = code + '\t}'
    return ast.parse(code).body[0]

def ind(noOfTab):
    return ''.ljust(4*noOfTab,' ')

if __name__ == "__main__":  # pragma: no cover
    main()
    
    