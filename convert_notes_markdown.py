import os
from bs4 import BeautifulSoup
from datetime import datetime

# Path to the input HTML file
input_file_path = 'D:/Downloads/flomo@Leche-20240623/Leche的笔记.html'  # 修改为下载的路径及文件名
output_directory = 'D:/Downloads/flomo@Leche-20240623/'  # 修改为输出的路径

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Read and parse the HTML file
with open(input_file_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find all memo entries
memos = soup.find_all('div', class_='memo')

# Group memos by date
memos_by_date = {}
for memo in memos:
    time_str = memo.find('div', class_='time').text
    date_str = time_str.split(' ')[0]  # Extract the date part
    content = memo.find('div', class_='content').find_all(['p', 'ol', 'ul'])

    if date_str not in memos_by_date:
        memos_by_date[date_str] = []

    memo_content = {
        'time': time_str,
        'tag': '',
        'body': ''
    }

    for element in content:
        element_html = str(element)
        element_html = element_html.replace('<br>', '  \n').replace('<br/>', '  \n')
        
        if element.name == 'ol':
            element_html = element_html.replace('<ol>', '').replace('</ol>', '').replace('<li>', '1. ').replace('</li>', '  \n')
        elif element.name == 'ul':
            element_html = element_html.replace('<ul>', '').replace('</ul>', '').replace('<li>', '- ').replace('</li>', '  \n')
        
        element_html_soup = BeautifulSoup(element_html, 'html.parser')
        element_text = element_html_soup.get_text('\n', strip=False)
        
        if element.name == 'p' and element_text.startswith('#'):
            memo_content['tag'] = element_text
        else:
            memo_content['body'] += element_text + '  \n'  # Add two spaces for Markdown line break
    
    images = memo.find_all('img')
    for img in images:
        memo_content['body'] += f'![image]({img["src"]})\n'
    
    memos_by_date[date_str].append(memo_content)

# Write each group of memos to a separate markdown file
for date_str, memos in memos_by_date.items():
    md_filename = f"{date_str}.md"
    md_filepath = os.path.join(output_directory, md_filename)
    with open(md_filepath, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# {date_str}\n\n")
        for memo in memos:
            md_file.write(f"## {memo['time']}\n")
            if memo['tag']:
                md_file.write(f"{memo['tag']}\n\n")  # Ensure tag is on its own line
            md_file.write(f"{memo['body']}\n")
            md_file.write('\n\n')  # Ensure two blank lines after each memo

print("Markdown files have been created successfully.")
