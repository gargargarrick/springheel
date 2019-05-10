import json, os, shutil

class EXpage:
    def __init__(self):
        self.headings = []

def gen_extra(i_path,o_path,extras_j,translated_strings):
    with open(extras_j,"r") as f:
      f_raw = f.read()
    j = json.loads(f_raw)
    extras = EXpage()
    extra_elements = []
    for cat in sorted(j.keys()):
        extras.headings.append(cat)
        subhead = "<h2>{cat}</h2>".format(cat=cat)
        extra_elements.append(subhead)
        for el in j[cat]:
            title = "<h3>{title}</h3>".format(title=el["title"])
            if el["type"] == "image":
                images = []
                for image in el["files"]:
                    images.append('<img src="{image}" alt="" />'.format(image=image))
                    shutil.copy(os.path.join(i_path,image),os.path.join(o_path,image))
                images = "".join(images)
                el_template = """<figure>{images}<figcaption>{desc}</figcaption></figure>""".format(images=images,desc=el["desc"])
            else:
                fils = []
                for fil in el["files"]:
                    fils.append("""<li><a href="{path}">{link}</a></li>""".format(path=fil["path"],link=fil["link"]))
                    shutil.copy(os.path.join(i_path,fil["path"]),os.path.join(o_path,fil["path"]))
                fils = "".join(fils)
                el_template = "<p>{desc}</p><ul>{fils}</ul>".format(desc=el["desc"],fils=fils)
            elem = "\n".join([title,el_template])
            extra_elements.append(elem)
    extra_combined = "\n".join(extra_elements)
    extras.content = extra_combined
    return(extras)
