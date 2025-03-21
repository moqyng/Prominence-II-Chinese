import json
import os
import shutil
from collections import defaultdict

# Unicode字符映射
UNICODE_MAPPING = {
    '\uF933': '\\uE001', '\uF934': '\\uE002', '\uF935': '\\uE003',
    '\uF936': '\\uE004', '\uF937': '\\uE005', '\uF938': '\\uE006',
    '\uF940': '\\uE007', '\uF941': '\\uE008', '\uF942': '\\uE009',
    '\uF943': '\\uE010', '\uF944': '\\uE011', '\uF945': '\\uE012',
    '\uF946': '\\uE013', '\uF947': '\\uE014', '\uF948': '\\uE015',
    '\uF949': '\\uE016', '\uF950': '\\uE017', '\uF951': '\\uE018',
    '\uF952': '\\uE019', '\uF953': '\\uE020', '\uF954': '\\uE021',
    '\uF955': '\\uE022', '\uF956': '\\uE023', '\uF957': '\\uE024',
    '\uF958': '\\uE025', '\uF959': '\\uE026'
}

def replace_unicode(text):
    if not isinstance(text, str):
        return text
    for old, new in UNICODE_MAPPING.items():
        text = text.replace(old, new)
    return text

def write_lang_file(file_path, translations):
    with open(file_path, 'wb') as f:
        # 手动构建JSON字符串,使用bytes写入以保持原始格式
        f.write(b'{\n')
        entries = []
        items = list(translations.items())
        for i, (key, value) in enumerate(items):
            # 只转义双引号,保持其他字符原样
            value = value.replace('"', '\\"').replace('\n', '\\n')
            entry = f'    "{key}": "{value}"'
            if i < len(items) - 1:
                entry += ','
            entries.append(entry.encode('utf-8'))
        f.write(b'\n'.join(entries))
        f.write(b'\n}\n')

def process_json_files(base_dir):
    all_translations = {}
    text_to_key = {}
    
    for root, dirs, files in os.walk(base_dir):
        # 处理 category.json
        category_file = os.path.join(root, "category.json")
        if os.path.exists(category_file):
            category_name = os.path.basename(root)
            
            with open(category_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "title" in data:
                title_text = data["title"]
                processed_text = replace_unicode(title_text)
                
                trans_key = f"puffish_skills.category.{category_name}.title"
                text_to_key[processed_text] = trans_key
                all_translations[trans_key] = processed_text
                
                data["title"] = {"translate": trans_key}
            
            with open(category_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            print(f"Processed and backed up: {category_file}")

        # 处理 definitions.json
        for file in files:
            if file == "definitions.json":
                file_path = os.path.join(root, file)
                category_name = os.path.basename(os.path.dirname(root))
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for skill_name, skill_data in data.items():
                    if "title" in skill_data:
                        title_text = skill_data["title"]
                        processed_text = replace_unicode(title_text)
                        
                        if processed_text not in text_to_key:
                            trans_key = f"puffish_skills.{category_name}.{skill_name}.title"
                            text_to_key[processed_text] = trans_key
                            all_translations[trans_key] = processed_text
                        
                        skill_data["title"] = {"translate": text_to_key[processed_text]}
                    
                    if "description" in skill_data:
                        desc_text = skill_data["description"]
                        processed_text = replace_unicode(desc_text)
                        
                        if processed_text not in text_to_key:
                            trans_key = f"puffish_skills.{category_name}.{skill_name}.description"
                            text_to_key[processed_text] = trans_key
                            all_translations[trans_key] = processed_text
                        
                        skill_data["description"] = {"translate": text_to_key[processed_text]}
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                print(f"Processed and backed up: {file_path}")
    
    # 生成语言文件
    lang_path = os.path.join(base_dir, "en_us.json")
    write_lang_file(lang_path, all_translations)
    print(f"Generated language file: {lang_path}")

def main():
    base_dir = r"d:\mc\mod\Prominence-II-Chinese\CNPack\config\puffish_skills\categories"
    process_json_files(base_dir)

if __name__ == "__main__":
    main()