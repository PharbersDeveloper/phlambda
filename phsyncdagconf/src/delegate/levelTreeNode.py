

class LevelTreeNode:

    def __init__(self, name, parent=None):
        super(LevelTreeNode, self).__init__()
        self.name = name
        self.parent = parent
        self.child = {}

    @property
    def path(self):
        """return path string (from root to current node)"""
        if self.parent:
            return '%s->%s' % (self.parent.path.strip(), self.name)
        else:
            return self.name

    def get_child(self, name, defval=None):
        # 获取当前节点子节点
        return self.child.get(name)

    def add_child(self, name, obj=None):
        # 添加子节点到当前节点
        if obj is None:
            obj = LevelTreeNode(name)
        obj.parent = self
        self.child[name] = obj
        return obj

    def del_child(self, name):
        if name in self.child:
            del self.child[name]

    def find_child(self, path, create=False):
        """find child node by path/name, return None if not found"""
        # convert path to a list if input is a string
        path = path if isinstance(path, list) else path.split("->")
        cur = self
        for sub in path:
            # search
            obj = cur.get_child(sub)
            if obj is None and create:
                # create new node if need
                obj = cur.add_child(sub)
            # check if search done
            if obj is None:
                break
            cur = obj
        return obj

    def items(self):
        return self.child.items()

    def dump(self, indent=0):
        """dump tree to string"""
        tab = '    '*(indent-1) + ' |- ' if indent > 0 else ''
        print('%s%s' % (tab, self.name))
        for name, obj in self.items():
            obj.dump(indent+1)

def get_latest_child(root_obj=None, max_level=-99999):
    if str(root_obj.items()) == "dict_items([])":
        print(root_obj.path)
        # line = root_obj.path.split()
        # root_level = len(line) - 1
        # if root_level > max_level:
        #     max_level = root_level
    for name, obj in root_obj.items():
        max_level = get_latest_child(obj, max_level)

    return max_level

if __name__ == '__main__':

    ds_001 = LevelTreeNode("ds_001")
    job1 = ds_001.add_child("job1")
    ds_002 = job1.add_child('ds_002')
    ds_003 = job1.add_child('ds_003')
    job2 = ds_002.add_child('job2')
    job3 = ds_003.add_child('job3')
    ds_004 = job2.add_child('ds_004')
    ds_005 = job2.add_child('ds_005')
    ds_006 = job3.add_child('ds_006')
    job4 = ds_006.add_child('job4')
    ds_007 = job4.add_child('ds_007')
    ds_001.dump()

    max_level = get_latest_child(ds_001)

    print(max_level)


    # for name, obj in job1.items():
    #     print(1111111111)
    #     print(type(name))
    #     print(name)

    # obj = root.find_child('a2 b3 c1')
    # print(obj.path.split())
    # print(type(obj.path))