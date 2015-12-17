file_name = 'Assignment 3.csv'

#import xlrd
import csv

def csv_from_excel():

    wb = xlrd.open_workbook('Assignment 3.xls')
    sh = wb.sheet_by_name('movie-row')
    your_csv_file = open(file_name, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

#csv_from_excel()

with open(file_name) as f:
    users = f.readline().replace('"','').split(',')[1:]
    user_ratings = dict()
    movie_ratings = dict()
    for user in users:
        user_ratings[user] = dict()
    for line in f.readlines():
        row = line.replace('"','').replace("'",'').replace('\n','').split(',')
        #print row, len(row)
        #raw_input()
        movie = row[0]
        ratings = row[1:]
        movie_ratings[movie] = dict()
        for i in range(len(ratings)):
            if len(ratings[i]) != 0:
                rating = float(ratings[i])
                movie_ratings[movie][users[i]] = rating
                user_ratings[users[i]][movie] = rating



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


