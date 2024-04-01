import sqlite3
import re
import datetime


def addUpdatedFileNameColumn():
    conn = sqlite3.connect('RecyclingCost.db')
    cursor = conn.cursor()

    # Add the updated_file_name column to PrintHistoryLinks table
    cursor.execute("ALTER TABLE PrintHistoryLinks ADD COLUMN update_date TEXT")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def updateFileNameColumn():
    conn = sqlite3.connect('RecyclingCost.db')
    cursor = conn.cursor()

    # Fetch the file_name column from PrintHistoryLinks table
    cursor.execute("SELECT file_name FROM PrintHistoryLinks")
    rows = cursor.fetchall()

    for row in rows:
        file_name = row[0]
        updated_file_name = processFileName(file_name)
        # Update the table with the modified file name
        cursor.execute("UPDATE PrintHistoryLinks SET update_date = ? WHERE file_name = ?",
                       (updated_file_name, file_name))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def processFileName(file_name):
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

    file_name = file_name.replace("ใบแจ้งราคารับซื้อสินค้า วัน", '')
    file_name = file_name.replace("(ราคาค้าปลีก)", '')

    file_name = file_name.replace('ที่', tmp)

    if tmp in file_name:
        getDate = file_name[file_name.find(tmp) + len(tmp):]
        date = int(getDate[0:3])

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
        else:
            return None

        year = int(getDate[-5:]) - 543
        x = datetime.datetime(year, month, date).date()
        dataDate = x.strftime("%d-%m-%Y")
        return dataDate
    else:
        return None


if __name__ == "__main__":
    addUpdatedFileNameColumn()
    updateFileNameColumn()
