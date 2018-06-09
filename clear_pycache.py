import os
import pprint
import glob

class ClearPycache():
    def get_path_list(self):
        project_path = input("enter the path:")
        find_dir_path = input("enter the Dir Name:")
        dir_list = os.listdir(project_path)
        path_list = []
        for path in dir_list:
            dir_path = project_path+"\\"+path+"\\"+find_dir_path

            if os.path.isdir(dir_path):
                path_list.append(dir_path)

        return path_list


    def actions(self):
        path_list = self.get_path_list()
        for path in path_list:
            # print(path)
            print('Count of file in dir:', len(os.listdir(path)))
            for file_name in os.listdir(path):
                if not "__init__" in file_name:
                    file_path = path + "\\" + file_name
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(file_path)


if __name__ == '__main__':
    cp = ClearPycache()
    cp.actions()