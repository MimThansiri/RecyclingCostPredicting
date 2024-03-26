import sqlite3
import pandas as pd
import datetime
# for searching matching string
import re
import numpy as np

csv_path = './cleanData.csv'
conn = sqlite3.connect('WasteSQL.db')
c = conn.cursor()
sql_syntax = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
c.execute(sql_syntax)
tableList = c.fetchall()


# print(tableList[1:])

# #get date from table name

def getDataDateSingle(table):
    tmp = "temporary word replace"
    jan = "มกราคม"
    feb = "กุมภาพันธ์"
    mar = "มีนาคม"
    apr = "เมษายน"
    may = "พฤษภาคม"
    jun = "มิถุนายน"
    jul = "กรกฏาคม"
    aug = "สิงหาคม"
    sep = "กันยายน"
    oct = "ตุลาคม"
    nov = "พฤศจิกายน"
    dec = "ธันวาคม"

    for tab in table:
        for t in tab:

            tab = tab.replace("ใบแจ้งราคารับซื้อสินค้า วัน", '')
            tab = tab.replace("(ราคาค้าปลีก)", '')
            tab = tab.replace('ที่', tmp)

            if tab.find(tmp) != -1:

                getDate = tab[tab.find(tmp) + len(tmp):]

                date = int(getDate[0:2])  # Adjusted to 2 digits since days are usually 2 digits
                month = 1  # Initialize to 1 as a default
                year = int(getDate[-5:]) - 543
                if re.search(jan, getDate):
                    month = 1
                elif re.search(feb, getDate):
                    month = 2
                elif re.search(mar, getDate):
                    month = 3
                elif re.search(apr, getDate):
                    month = 4
                elif re.search(may, getDate):
                    month = 5
                elif re.search(jun, getDate):
                    month = 6
                elif re.search(jul, getDate):
                    month = 7
                elif re.search(aug, getDate):
                    month = 8
                elif re.search(sep, getDate):
                    month = 9
                elif re.search(oct, getDate):
                    month = 10
                elif re.search(nov, getDate):
                    month = 11
                elif re.search(dec, getDate):
                    month = 12

                x = datetime.datetime(year, month, date).date()
                dataDate = x.strftime("%d-%m-%Y")
                return dataDate

concatenated_df = pd.DataFrame([])
for tabl in tableList[1:]:
    tb_name = "'" + tabl[0] + "'"
    df = pd.read_sql_query("select * from " + tb_name, conn)
    df.rename(columns={"('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ชนิดสินค้า')": 'material'
        , "('ประเภทโลหะที่มีค่าสูง / Nonferrous metals', 'ราคา / หน่วย')": 'price'}, inplace=True)
    # transform adding column date
    df['date'] = getDataDateSingle(tabl)
    #         filter search by material condition
    filteredDf = df[df['material'] == 'อลูมิเนียมแผ่นเพจ']
    # print(filteredDf)

    if filteredDf.empty:
        continue
    else:
        #             combine all filtered data to one dataframe
        concatenated_df = pd.concat([concatenated_df, filteredDf], ignore_index=True)

# sort data -> sort แล้วไม่ต้องใส่ก็ได้
# concatenated_df.sort_values('price',ascending=True)

# load result to csv
concatenated_df.to_csv(csv_path, index=False)