import xlrd
import csv

def csv_from_excel(filein, fileout, worksheet):

    wb = xlrd.open_workbook(filein)
    sh = wb.sheet_by_name(worksheet)
    your_csv_file = open(fileout, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

csv_from_excel('Assignment 6.xls','Assignment 6 items .csv', 'Items')
csv_from_excel('Assignment 6.xls','Assignment 6 users .csv', 'Users')