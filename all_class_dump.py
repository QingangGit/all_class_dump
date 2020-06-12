import os
import sys,getopt
import zipfile

class all_dump:
    def __init__(self,ipa_path):
        self.li = []
        self.ipa_path = ipa_path
        self.father_path = ''
        self.pkg_father_path = ''

    def start_class_dump(self):
        self.path_config()
        unzip_single(self.ipa_path, self.father_path)
        self.pri_all_file( self.pkg_father_path)
        self.do_class_dump()

    def path_config(self):
        self.father_path = os.path.abspath(os.path.dirname(self.ipa_path))
        self.pkg_father_path = self.father_path + '/Payload'

    def pri_all_file(self,dir):
        names = os.listdir(dir)  # 获取当前目录下所有文件名及目录名
        for name in names:
            full_name = dir + '/' + name  # 拼接成完整路径
            if os.path.isdir(full_name):
                self.pri_all_file(full_name)  # 递归遍历子目录下文件及目录
            else:
                res = is_macho_file(full_name)
                if res==True:
                    self.li.append(full_name)

    def do_class_dump(self):
        for macho_file in self.li:
            macho_father_path = os.path.abspath(os.path.dirname(macho_file))
            p = macho_father_path.split('/')[-1]
            p = p.split('.')[0]
            out_path = self.father_path + '/dump_heads/' + p
            class_dump_(macho_file,out_path)



def class_dump_(need_dump_p,dump_out_p):
    # need_dump_address = '/Users/qin/Desktop/越狱砸壳系列/Payload/qqlive.app/Frameworks/YYModel.framework'
    # dump_out_address = '/Users/qin/Desktop/md/YYModel'

    action = 'class-dump -H ' +  need_dump_p + ' -o ' + dump_out_p
    print(action)
    os.system(action)


def is_macho_file(file):
    action = 'file ' + file
    try:
        p = os.popen(action).read()
        res = p.find('Mach-O')
        if res > 0:
            return True
        else:
            return False
    except:
        return False

def unzip_single(src_file, dest_dir):

    zf = zipfile.ZipFile(src_file)
    try:
        zf.extractall(path=dest_dir)
    except RuntimeError as e:
        print(e)
    zf.close()

if __name__ == '__main__':

    ipa_path = ''
    opts, args = getopt.getopt(sys.argv[1:], '')

    if len(args) <= 0:
        print('need ipa_path')
        sys.exit(-1)

    ipa_path = args[0]

    all_dump_m = all_dump(ipa_path)

    all_dump_m = all_dump(ipa_path)
    all_dump_m.start_class_dump()


