import requests
from bs4 import BeautifulSoup
from datetime import datetime

MODE = "Markdown"

def get_devo(date=None):
    
    def format_section(section):
        text = ''
        header = True
        for part in section.children:
            part_text = part.extract().get_text()
            if header:
                header = False
                text += format_text(MODE, "bold").format(part_text) + '\n\n'
            else:
                text += part_text + '\n\n'
        return text[:-2]
    
    url = "https://lovesingapore.org.sg/40day/2020/"
    if date:
        formatted_date = date_to_datetime(date).strftime("%B-%#d").replace("-0", "-")
        url += formatted_date
    else:
        url += "july-20/"
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    date = html_soup.find('div', class_ = 'et_pb_module et_pb_text et_pb_text_0 et_pb_text_align_left et_pb_bg_layout_light').div.extract().get_text()
    word_section = html_soup.find('div', class_ = 'et_pb_with_border et_pb_module et_pb_text et_pb_text_1 et_pb_text_align_left et_pb_bg_layout_light').div
    prayer_section = html_soup.find('div', class_ = 'et_pb_with_border et_pb_module et_pb_text et_pb_text_8 et_pb_text_align_left et_pb_bg_layout_light').div

    devo = {"date": format_text(MODE, "italics").format(date), "word": format_section(word_section), "prayer": format_section(prayer_section)}
    return devo

def get_devo_chunks(date=None):
    CHARACTER_LIMIT = 4096
    
    chunks = []
    devo = get_devo(date)
    first_chunk = devo["date"]
    
    if len(first_chunk + devo["word"]) + 2 < CHARACTER_LIMIT:
        first_chunk += '\n\n' + devo["word"]
        chunks.append(first_chunk)
    else:
        chunks.extend(break_into_chunks(first_chunk + '\n\n' + devo["word"] + '\n\n'))

    if len(chunks[-1] + devo["prayer"]) + 2 < CHARACTER_LIMIT:
        chunks[-1] += '\n\n' + devo["prayer"]
    else:
        chunks.extend(break_into_chunks(devo["prayer"], CHARACTER_LIMIT))

    return chunks

def get_parse_mode():
    return MODE

def format_text(mode, format):
    # Supported modes: Markdown
    # Supported formats: Bold, Italics
    formatting = {
        "bold": "*{}*",
        "italics": "_{}_"
    }
    return formatting[format]

def break_into_chunks(string, length):
    return list(string[0+i:length+i] for i in range(0, len(string), length))

def date_to_datetime(str_date):
    str_date = str_date.strip()
    month_and_date = str_date.split(' ')
    if len(month_and_date) != 2 or (len(month_and_date) == 2 and not is_valid(month_and_date[0], month_and_date[1])):
        raise ValueError
    date = datetime.strptime(str_date, "%B %d").replace(year=2020)
    return date
        
def is_valid(month, date):
    if (month.lower() != "july" and month.lower() != "august") or not date.isdigit():
        print("Invalid month or date is string")
        return False
    if date.lstrip('0') == '':
        return False
    num_date = int(date.lstrip('0'))
    if month.lower() == "july":
        if num_date < 1 or num_date > 31:
            print("July error")
            return False
    elif month.lower() == "august":
        if num_date < 1 or num_date > 9:
            print("August error")
            return False
    return True
