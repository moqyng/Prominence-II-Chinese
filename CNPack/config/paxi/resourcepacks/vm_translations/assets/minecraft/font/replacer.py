import json
import re

def find_existing_unicode_chars(content):
    """找出文件中实际存在的 F933-F959 范围内的 Unicode 字符"""
    pattern = r'\\uF(?:93[3-9]|94[0-9]|95[0-9])'
    matches = re.findall(pattern, content)
    return sorted(list(set(matches)))

def create_mapping(existing_chars):
    """为实际存在的字符创建映射"""
    new_chars = [f'\\uE{i:03d}' for i in range(1, len(existing_chars) + 1)]
    return dict(zip(existing_chars, new_chars))

def remap_unicode_chars(input_file, output_file):
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找出实际存在的字符
    existing_chars = find_existing_unicode_chars(content)
    print(f"找到的Unicode字符: {', '.join(existing_chars)}")
    
    # 创建映射
    char_map = create_mapping(existing_chars)
    print("\n映射关系:")
    for old, new in char_map.items():
        print(f"{old} -> {new}")
    
    # 使用正则表达式进行替换
    pattern = '|'.join(map(re.escape, char_map.keys()))
    new_content = re.sub(pattern, lambda m: char_map[m.group()], content)
    
    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"\n替换完成！新文件已保存为: {output_file}")

# 使用示例
input_file = r"d:\mc\mod\Prominence-II-Chinese\CNPack\config\paxi\resourcepacks\vm_translations\assets\minecraft\font\default.json"
output_file = r"d:\mc\mod\Prominence-II-Chinese\CNPack\config\paxi\resourcepacks\vm_translations\assets\minecraft\font\default_new.json"

remap_unicode_chars(input_file, output_file)
'''
\uF933 -> \uE001
\uF934 -> \uE002
\uF935 -> \uE003
\uF936 -> \uE004
\uF937 -> \uE005
\uF938 -> \uE006
\uF940 -> \uE007
\uF941 -> \uE008
\uF942 -> \uE009
\uF943 -> \uE010
\uF944 -> \uE011
\uF945 -> \uE012
\uF946 -> \uE013
\uF947 -> \uE014
\uF948 -> \uE015
\uF949 -> \uE016
\uF950 -> \uE017
\uF951 -> \uE018
\uF952 -> \uE019
\uF953 -> \uE020
\uF954 -> \uE021
\uF955 -> \uE022
\uF956 -> \uE023
\uF957 -> \uE024
\uF958 -> \uE025
\uF959 -> \uE026
'''