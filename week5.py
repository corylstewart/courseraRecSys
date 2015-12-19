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
        #else:
        #   for i in range(1,len(row)-1):
        #       movies[movies_list[i-1]]['ratings']['L2'] = row[i]

#using user dictionary create movie dictionary
L2 = dict()
L2['ratings'] = dict()
L2['norm'] = dict()
for user in users:
    for movie in users[user]['ratings']:
        movies[movie]['ratings'][user] = users[user]['ratings'][movie]
    for movie in users[user]['norm']:
        movies[movie]['norm'][user] = users[user]['norm'][movie]
for movie in movies:
    r = 0.
    n = 0.
    for user in movies[movie]['norm']:
        r += pow(movies[movie]['ratings'][user],2)
        n += pow(movies[movie]['norm'][user],2)
    L2['ratings'][movie] = pow(r,0.5)
    L2['norm'][movie] = pow(n,0.5)


#create the movie movie correlations
corr = dict()
corr['ratings'] = dict()
corr['norm'] = dict()

def cal_corr(movie1, movie2, movies):
    tot1r = 0.
    tot2r = 0.
    tot1n = 0.
    tot2n = 0.
    count = 0.
    for user in movies[movie1]['norm']:
        if user in movies[movie2]['norm']:
            tot1r += movies[movie1]['ratings'][user]
            tot2r += movies[movie2]['ratings'][user]
            tot1n += movies[movie1]['norm'][user]
            tot2n += movies[movie2]['norm'][user]
            count += 1
    if count == 0:
        return (0, 0)
    mean1r = tot1r/count
    mean2r = tot2r/count
    mean1n = tot1n/count
    mean2n = tot2n/count
    tot1r = 0.
    tot2r = 0.
    tot1n = 0.
    tot2n = 0.
    for user in movies[movie1]['ratings']:
        if user in movies[movie2]['ratings']:
            tot1r += pow((movies[movie1]['ratings'][user] - mean1r),2)
            tot2r += pow((movies[movie2]['ratings'][user] - mean2r),2)
            tot1n += pow((movies[movie1]['norm'][user] - mean1n),2)
            tot2n += pow((movies[movie2]['norm'][user] - mean2n),2)
    count -= 1
    if count == 0:
        return (0, 0)
    std1r = pow((tot1r/count), 0.5)
    std2r = pow((tot2r/count), 0.5)
    std1n = pow((tot1n/count), 0.5)
    std2n = pow((tot2n/count), 0.5)
    totr = 0.
    totn = 0.
    for user in movies[movie1]['ratings']:
        if user in movies[movie2]['ratings']:
            totr += (movies[movie1]['ratings'][user]-mean1r)*(movies[movie2]['ratings'][user]-mean2r)
            totn += (movies[movie1]['norm'][user]-mean1n)*(movies[movie2]['norm'][user]-mean2n)
    corrr = totr/(std1r*std2r*count)
    corrn = totn/(std1n*std2n*count)
    return corrr, corrn

#print cal_corr('"1: Toy Story (1995)"', '"34: Babe (1995)"', movies)

#create cos similarities

def cos_sim(movie1, movie2, movies):
    abr = 0.
    ar = 0.
    br = 0.
    abn = 0.
    an = 0.
    bn = 0.
    for user in users:
        if user in movies[movie1]['ratings'] and user in movies[movie2]['ratings']:
            abr += movies[movie1]['ratings'][user] * movies[movie2]['ratings'][user]
            abn += movies[movie1]['norm'][user] * movies[movie2]['norm'][user]
        if user in movies[movie1]['ratings']:
            ar += movies[movie1]['ratings'][user] * movies[movie1]['ratings'][user]
            an += movies[movie1]['norm'][user] * movies[movie1]['norm'][user]
        if user in movies[movie2]['ratings']:
            br += movies[movie2]['ratings'][user] * movies[movie2]['ratings'][user]
            bn += movies[movie2]['norm'][user] * movies[movie2]['norm'][user]
    cr = abr/(pow(ar,.5)*pow(br,.5))
    cn = abn/(pow(an,.5)*pow(bn,.5))
    return cr, cn

#cos_sim('"1: Toy Story (1995)"', '"1210: Star Wars: Episode VI - Return of the Jedi (1983)"', movies)
sim = dict()
sim['ratings'] = dict()
sim['norm'] = dict()
for i in range(len(movies_list)-1):
    movie1 = movies_list[i]
    if movie1 not in sim['ratings']:
        sim['ratings'][movie1] = dict()
        sim['norm'][movie1] = dict()
    for j in range(i,len(movies_list)):
        movie2 = movies_list[j]
        if movie2 not in sim['ratings']:
            sim['ratings'][movie2] = dict()
            sim['norm'][movie2] = dict()
        r, n = cos_sim(movie1, movie2, movies)
        sim['ratings'][movie1][movie2] = r
        sim['norm'][movie1][movie2] = n
        sim['ratings'][movie2][movie1] = r
        sim['norm'][movie2][movie1] = n

best_matches_r = list()
best_matches_n = list()
for movie in sim['ratings']['"1: Toy Story (1995)"']:
    best_matches_r.append((sim['ratings']['"1: Toy Story (1995)"'][movie], movie))
    best_matches_n.append((sim['norm']['"1: Toy Story (1995)"'][movie], movie))
best_matches_r.sort(reverse=True)
best_matches_n.sort(reverse=True)
print 'Ratings'
for movie in best_matches_r[1:6]:
    break
    print movie

print ''
print 'Norm'
for movie in best_matches_n[1:6]:
    break
    print movie


def movie_predictions(user, movies, sim, type):
    other_movies = list()
    for movie1 in movies:
        tot = 0.
        count = 0.
        for movie2 in movies:
            if user in movies[movie2][type] and sim[type][movie1][movie2] > 0:
                tot += movies[movie2][type][user] * sim[type][movie1][movie2]
                count += sim[type][movie1][movie2]
        if count != 0:
            other_movies.append((tot/count, movie1))
    other_movies.sort(reverse=True)
    return other_movies

user = '5277.0'
print ''
print user, 'ratings'
predictions = movie_predictions(user, movies, sim, 'ratings') 
for p in predictions[:5]:
    print p

print ''
print user, 'norm'
predictions = movie_predictions(user, movies, sim, 'norm') 
for p in predictions[:5]:
    print p

