from bs4 import BeautifulSoup
import requests

presupuesto = float("50")
url = 'https://www.joyeriasanchez.com/16-pendientes'
data = requests.get(url)
soup = BeautifulSoup(data.content, 'lxml')
divs = soup.find('div', {'class': 'product_list'})
children = divs.find_all('div',{'class': 'ajax_block_product'})
output = ''
for child in children:
    try:        
        price = child.find('span', {'class':'price product-price'}).text
        price = float((price.split(' ')[1]).replace(',','.'))
        
        # image_link = child.find('a', {'class':'product_img_link'}).get('href') 
        image_link = child.find('img', {'class':'img-responsive'}).get('src')
        title = child.find('p',{'class':'product-desc'}).text
              
        
        if price <= presupuesto:
            a = (f'{image_link}\n{title}\n{price}$')
            output = f'{output}\n{a}'
            
            
    except:
        pass
        
print(output)
