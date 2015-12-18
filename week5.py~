file_name = 'Assignment 5.csv'

import xlrd
import csv

def csv_from_excel():

    wb = xlrd.open_workbook('Assignment 5.xls')
    sh = wb.sheet_by_name('Ratings')
    your_csv_file = open(file_name, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

#csv_from_excel()

#read from file and create users dictionary
with open(file_name, 'U') as f:
    line = f.readline().replace('\n','')#.replace('"','')
    movies_list = line.split(',')[1:-1]
    movies_list = [movie for movie in movies_list if movie[:4] != ' The']
    movies = dict()
    for movie in movies_list:
        movies[movie] = dict()
        movies[movie]['ratings'] = dict()
        movies[movie]['norm'] = dict()
    users = dict()
    for line in f.readlines():
        row = line.replace('\n','').replace('"', '').split(',')
        if row[0] != 'L2':
            user = row[0]
            mean = float(row[-1])
            users[user] = dict()
            users[user]['ratings'] = dict()
            users[user]['norm'] = dict()
            users[user]['mean'] = mean
            for i in range(1,len(row)-1):
                if row[i] != '':
                    users[user]['ratings'][movies_list[i-1]] = float(row[i])
                    users[user]['norm'][movies_list[i-1]] = float(row[i]) - mean
        else:
            for i in range(1,len(row)-1):
                movies[movies_list[i-1]]['ratings']['L2'] = row[i]

#using user dictionary create movie dictionary
for user in users:
    for movie in users[user]['ratings']:
        movies[movie]['ratings'][user] = users[user]['ratings'][movie]
    for movie in users[user]['norm']:
        movies[movie]['norm'][user] = users[user]['norm'][movie]
for movie in movies:
    n = 0
    for user in movies[movie]['norm']:
        n += pow(movies[movie]['norm'][user],2)
    movies[movie]['norm']['L2'] = pow(n,0.5)


#create the movie movie correlations
corr = dict()


'''



def cal_corr(user1, user2, user_ratings):
    tot1 = 0.
    tot2 = 0.
    count = 0.
    for movie in user_ratings[user1]:
        if movie in user_ratings[user2]:
            tot1 += user_ratings[user1][movie]
            tot2 += user_ratings[user2][movie]
            count += 1
    if count == 0:
        return 0
    mean1 = tot1/count
    mean2 = tot2/count
    tot1 = 0.
    tot2 = 0.
    for movie in user_ratings[user1]:
        if movie in user_ratings[user2]:
            tot1 += pow((user_ratings[user1][movie] - mean1),2)
            tot2 += pow((user_ratings[user2][movie] - mean2),2)
    count -= 1
    if count == 0:
        return 0
    std1 = pow((tot1/count), 0.5)
    std2 = pow((tot2/count), 0.5)
    tot = 0
    for movie in user_ratings[user1]:
        if movie in user_ratings[user2]:
            tot += (user_ratings[user1][movie]-mean1)*(user_ratings[user2][movie]-mean2)
    return tot/(std1*std2*count)

means = dict()
for user in user_ratings:
    total = 0.
    count = 0.
    for movie in user_ratings[user]:
        total += user_ratings[user][movie]
        count += 1
    means[user] = total/count



corr = dict()
for user1 in user_ratings:
    corr[user1] = dict()
    for user2 in user_ratings:
        if user1 != user2:
            corr[user1][user2] = cal_corr(user1,user2,user_ratings)

def get_neib(node, corr):
    neib = list()
    for n in corr[node]:
        neib.append((corr[node][n], node, n))
    neib.sort(reverse=True)
    return neib[:5]

def make_prediction(movie, user, neib, user_ratings):
    total = 0.
    count = 0.
    for n in neib:
        if movie in user_ratings[n]:
            total += user_ratings[n][movie] * corr[user][n]
            count += corr[user][n]
    if count != 0:
        return total/count
    else:
        return 0

def make_all_predictions(user, user_ratings, movie_ratings):
    neib = list()
    for n in get_neib(user, corr):
        neib.append(n[2])
    movies = list()
    for movie in movie_ratings:
        movies.append((make_prediction(movie, user, neib, user_ratings), movie))
    movies.sort(reverse=True)
    tot = min(len(movies),5)
    print ''
    print 'Non-Weighted Results'
    print 'User: ', user
    for i in range(tot):
        print 'Movie: ', movies[i][1].split(':')[0],' Prediction: ',movies[i][0]
 
node1 = '3867.0'
node2 = '89.0'

make_all_predictions(node1, user_ratings, movie_ratings)
make_all_predictions(node2, user_ratings, movie_ratings)


def make_weighted_prediction(movie, user, neib, user_ratings):
    total = 0.
    count = 0.
    for n in neib:
        if movie in user_ratings[n]:
            total += (user_ratings[n][movie] - means[n]) * corr[user][n]
            count += corr[user][n]
    if count != 0:
        return means[user] + total/count
    else:
        return 0

def make_weighted_predictions(user, user_ratings, movie_ratings):
    neib = list()
    for n in get_neib(user, corr):
        neib.append(n[2])
    movies = list()
    for movie in movie_ratings:
        movies.append((make_weighted_prediction(movie, user, neib, user_ratings), movie))
    movies.sort(reverse=True)
    tot = min(len(movies),5)
    print ''
    print 'Weight Results'
    print 'User: ', user
    for i in range(tot):
        print 'Movie: ', movies[i][1].split(':')[0],' Prediction: ',movies[i][0]


make_weighted_predictions(node1, user_ratings, movie_ratings)
make_weighted_predictions(node2, user_ratings, movie_ratings)


'''