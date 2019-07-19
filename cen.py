import os

lis = os.listdir("./output")
lis_dict = {
    file_name: os.path.getsize(f"./output/{file_name}") / 1000 for file_name in lis
}
print(lis_dict)
