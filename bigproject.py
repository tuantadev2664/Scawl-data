import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def processingData(link: str):
    print(link)
    response = requests.get(link)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    name_element = soup.find('h1', class_='detail-name')
    product_name = name_element.text.strip() if name_element else 'N/A'

    product_code_element = soup.find('b', id='product-code')
    product_code = product_code_element.text.strip() if product_code_element else 'N/A'

    status_parent = soup.find('div', class_="col-md-6")
    status_children = status_parent.find_next_siblings('div', class_="col-md-6") if status_parent else []
    for child in status_children:
        status_element = child.find('b')
        if status_element:
            status = status_element.text.strip()
            break
    else:
        status = 'N/A'

    price_element = soup.find('div', class_='detail-price')
    price = price_element.contents[0].strip() if price_element and price_element.contents else 'N/A'

    old_price_element = price_element.find('span') if price_element else None
    old_price = old_price_element.text.strip() if old_price_element else 'N/A'

    summary_element = soup.find('div', class_='detail-summary')
    paragraphs = [p.text.strip() for p in summary_element.find_all('p')] if summary_element else []

    colorLinks = []
    links = soup.select('.detail-colors > a > img')
    for link in links:
        if link['src']:
            colorLinks.append(link['src'])

    button_elements = soup.find_all('button', class_="button-size")
    button_contents = [button.text.strip() for button in button_elements]

    product_img_links = []
    imglinks = soup.select('.product-thumbs img')
    for link in imglinks:
        if link['src']:
            product_img_links.append(link['src'])

    product_array = [product_name, product_code, status, price, old_price, paragraphs, colorLinks, button_contents, product_img_links]
    return product_array


base = 'https://monatabluelight.com/'
productLinks = []

for i in range(10):
    resp = requests.get(base + 'san-pham/page-' + str(i) + '.html')
    soup = BeautifulSoup(resp.content, "html.parser")
    links = soup.select('.product-item > a')
    for link in links:
        if link['href']:
            productLinks.append(link['href'])

list_product = []

for link in productLinks:
    product_data = processingData(link)
    list_product.append(product_data)
    # print(product_data)

# workbook = Workbook()
# sheet = workbook.active
# sheet.append(['product_name', 'product_code', 'status', 'price', 'old_price', 'paragraphs', 'colorLinks', 'button_contents', 'product_img_links'])
# for product_array in list_product:
#     sheet.append(product_array)
# workbook.save('data.xlsx')
filename = 'data.txt'

with open(filename, 'w', encoding='utf-8') as file:
    file.write('product_name,product_code,status,price,old_price,paragraphs,colorLinks,button_contents,product_img_links\n')
    for product_array in list_product:
        if not product_array[5]:
            product_array[5] = 'N/A'
        line = ','.join(map(str, product_array))
        file.write(line + '\n')

print(f"Data has been written to {filename}.")