import requests
import json
import sys, os


def updateFile(url, name):
    cmd = "wget {0} -O {1}".format(name, url)
    print(cmd)
    os.system(cmd)
    msg = "Update file {0} after checksum changed.".format(name)
    git_cmd = "git commit -m 'Update file {0} after checksum changed.' {0}".format(name)
    os.system(git_cmd)
    print(git_cmd)

    os.system('git push')

def updateDescFile(path, desc):
    with open(path,'w') as f :
        f.write(json.dumps(desc))

    git_cmd = "git commit -m 'Update file {0} after checksum changed.' {0}".format(path)
    os.system(git_cmd)
        os.system('git push')

if __name__ == '__main__' :

    r = requests.get('https://www.data.gouv.fr/api/1/datasets/5c34c4d1634f4173183a64f1')

    r.raise_for_status()
    
    res = r.json()

    resources = res['resources']

    for resource in resources:


        title = resource['title']
        hashType = resource['checksum']['type']
        hash = resource['checksum']['value']
        url = resource['latest']

        desc_file = title + "_desc"

        #TODO : check if file exists
        with open(desc_file,'r') as f :
            previous_desc = json.load(f)

            previous_hashType = previous_desc['checksum']['type']

            if previous_hashType != hashType:
                sys.exit("Not the same Hash type for file : " + title)

            previous_hash = previous_desc['checksum']['value']
            if hash != previous_hash:
                print(title + " : Error desync on hash.")
                updateFile(url, title)
                updateDescFile(desc_file, resource)
            else :
                print(title + ": Ok!")





