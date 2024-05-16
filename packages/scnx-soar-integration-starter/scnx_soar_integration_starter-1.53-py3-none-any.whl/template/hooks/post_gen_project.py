import os, json
from jsonmerge import merge

def main():
    print("********** POST GENERATION HOOK *************")
    cur_dir = os.path.abspath(os.path.curdir)
    pyFile = "{{cookiecutter.integration_id}}" + ".py"
    classFilePath = os.path.join(cur_dir, "app", cur_dir.name + '.py')
    print(classFilePath) 


    try :
        meta = open(os.path.join(cur_dir, "integration_meta.json")).read()
        definition = open(os.path.join(cur_dir, "integration_definition.json")).read()
        info_json = merge(meta, definition)
        functions = json.loads(info_json)['functions']
        pyFile = open(classFilePath, "a")
        for function in functions:
            method = ["\n\n\n",ind(1) + "def " + function['name'] + "(): \n", ind(2) + "# Write you logic to handle this action \n", ind(2) + "pass"]
            pyFile.writelines(method)
        pyFile.close()
    except Exception as e:
        print(e)

def ind(noOfTab):
    return ''.ljust(4*noOfTab,' ')


if __name__ == '__main__':
    # sys.exit(main())
    pass