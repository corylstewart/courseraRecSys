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

#csv_from_excel('Assignment 6.xls','Assignment 6 items .csv', 'Items')
#csv_from_excel('Assignment 6.xls','Assignment 6 users .csv', 'Users')

#create items dictionary
filename = 'Assignment 6 items .csv'
movies = dict()
with open(filename, 'U') as f:
    features = f.readline().replace('"','').replace('\n','').split(',')
    weights = ['',''] + [float(x) for x in f.readline().replace('"','').replace('\n','').split(',')[2:]]
    f.readline()
    movies = dict()
    for line in f.readlines():
        row = line.split(',')
        movies[row[0]] = dict()
        movies[row[0]]['name'] = row[1]
        movies[row[0]]['features'] = dict()
        for i in range(2,len(row)):
            movies[row[0]]['features'][features[i]] = float(row[i].replace('"','').replace('\n',''))

#create users dictionary
filename = 'Assignment 6 users .csv'
users = dict()
with open(filename, 'U') as f:
    features2 = f.readline().replace('"','').replace('\n','').split(',')
    users = dict()
    for line in f.readlines():
        row = line.split(',')
        users[row[0]] = dict()
        users[row[0]]['features'] = dict()
        for i in range(1,len(row)):
            users[row[0]]['features'][features2[i]] = float(row[i].replace('"','').replace('\n',''))

#create final features and weights lists 
features = features[2:]
weights = weights[2:]

def make_prediction(user, movies, users, features, weights):
    #f = list()
    #for i in range(len(features)):
    #    f.append((weights[i]*users[user]['features'][features[i]], features[i]))
    #f.sort(reverse=True)
    #top = f[:2]
    l = list()
    for movie in movies:
        total = 0.
        for i in range(len(features)):
            feature = features[i]
            f = users[user]['features'][feature]
            w = weights[i]
            m = movies[movie]['features'][feature]
            #print movie,m,f,w
            total += f * w * m
            #raw_input()
        l.append((total, movie))
    l.sort(reverse=True)
    for i in range(5):
        print l[i]

make_prediction('"4469.0"', movies, users, features, weights)