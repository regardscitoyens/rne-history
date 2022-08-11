import requests
import json
import sys, os


def updateFile(url, name):
    cmd = "wget -nv {0} -O {1}".format(url, name)
    os.system(cmd)


def updateDescFile(path, desc):
    with open(path,'w') as f :
        f.write(json.dumps(desc))


if __name__ == '__main__' :

    r = requests.get('https://www.data.gouv.fr/api/1/datasets/5c34c4d1634f4173183a64f1')
    r.raise_for_status()
    res = r.json()
    resources = res['resources']

    index = 1
    push = False

    for resource in resources:

        if not resource['title'].endswith(".csv"):
            resource['title'] += ".csv"

        title = "%d-%s" % (index, resource['title'])
        hashType = resource['checksum']['type']
        hash = resource['checksum']['value']
        url = resource['latest']

        desc_file = title + "_desc"

        if os.path.exists(desc_file):
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
                    git_cmd = "git commit -m 'Update file %s after checksum changed.' %s %s" % (title, title, desc_file)
                    os.system(git_cmd)
                    push = True

        else:
            print("Tracking new registre: " + title)
            updateFile(url, title)
            updateDescFile(desc_file, resource)

        index += 1

    if push:
        os.system('git push')

