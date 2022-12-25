import re
from bs4 import BeautifulSoup
import xlwt
import xlrd

wb = xlwt.Workbook()
# 添加一个表
ws = wb.add_sheet('test')


fileObject = open('D:\\orderMg\\order.html', mode='r', encoding='utf-8')
soup = BeautifulSoup(fileObject, 'lxml')
dataList = []

order = ""
name = ""
phone = ""
date = ""
price = ""
i = 0;

for str in soup.findAll(re.compile('tr')):
    i += 1
    if (str['data-row-key'].find('child') >= 0):
        infos = list(str.findAll(re.compile('td')))
        phone = list(list(infos[5].findAll(re.compile('span')))[0].children)[0]
        name = list(list(infos[5].findAll(re.compile('div')))[2].children)[0].strip()
        price = list(list(infos[4].findAll('div'))[1].descendants)[2].replace('\n','')
    else:
        if (len(list(str.findAll('span'))) < 3) :
            i-=1
            order,name,phone,price,data = "","","","",""
            continue
        order = str['data-row-key']
        time = list(list(list(str.findAll('td'))[1].findAll('span'))[2].children)[0].replace(' ','').replace('\n','').replace('下单时间','').strip()
        date = time[0:10] + " " + time[10:]

    if (i%2 == 0):
        dataRow = {'order': order, 'name': name, 'phone': phone,'price': price, 'date': date}
        dataList.append(dataRow)

# 把数据写入到excel文件中
ws.write(0,0,"订单编号")
ws.write(0,1,"客户名称")
ws.write(0,2,"联系电话")
ws.write(0,3,"价格")
ws.write(0,4,"下单时间")
x=1
for dataRow in dataList:
    y = 0
    for data in dataRow:
        ws.write(x, y, dataRow[data])
        y+=1
    x+=1

wb.save('D:\\orderMg\\order.xls')
print('导出成功')