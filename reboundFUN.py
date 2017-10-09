import pandas as pd

############################
# Import and organize data
############################
with open("201617totalPBP.csv", 'r') as myFile:
    dataLines = myFile.read().splitlines()

data_temp = []
for z in range(1, len(dataLines)):
    data_temp.append(dataLines[z].split(','))

data = []
for i in range(len(data_temp)):
    # x[0] away unit, x[1] home unit, x[2] event, x[3] player, x[4] play type, x[5] season type, x[6] points, x[7] team
    data.append([data_temp[i][3:8], data_temp[i][8:13], data_temp[i][21], data_temp[i][31], data_temp[i][37],
                 data_temp[i][1], data_temp[i][32], data_temp[i][20]])

print len(dataLines), len(data_temp), len(data)

###################################
# 1) Who boarded their own misses?
###################################
boarders = {}
misses = {}
index = 1
for x in data[2:-1]:
    index += 1
    away = x[0]
    home = x[1]

    if x[2] == "miss":
        if x[3] not in misses:
            misses[x[3]] = 1
        if x[3] in misses:
            misses[x[3]] += 1

    if (x[2] == "miss") and (data[index+1][2] == "rebound"):
        if x[3] == data[index+1][3]:
            # print x[5], x[3], data[index+1][4], x[4]
            if x[3] not in boarders:
                boarders[x[3]] = 1
            if x[3] in boarders:
                boarders[x[3]] += 1

boarder_arr = []
for p in boarders:
    boarder_arr.append((p, float(boarders[p])/misses[p]))
boarder_arr.sort(key=lambda tup: tup[1], reverse=True)

# Prep results for output
print "Boarding their own missed FGs"
output_framer = []
r = 1
for i, rating in enumerate(boarder_arr):
    name = "{}".format(rating[0])
    # filtering out low usage
    if (name in misses) and (misses[name] > 75):
        output_framer.append([r, name, "{}".format(rating[1])])
        print [r, "{}".format(rating[0]), "{}".format(rating[1])]
        r += 1

output_df = pd.DataFrame(output_framer, columns=['Rank', 'Player', 'Own-OREB%'])
output_df.to_csv("OwnMissOREB.csv")


####################################################
# 2) Which players' OREBS led to most points? -Team
####################################################
boarder_poss = {}
points = {}
index = 1
for x in data[2:-1]:
    index += 1
    away = x[0]
    home = x[1]

    if x[4] == "rebound offensive":

        # count possessions created by offensive rebounds
        if x[7] not in boarder_poss:
            boarder_poss[x[7]] = 1
            points[x[7]] = 0
        if x[7] in boarder_poss:
            boarder_poss[x[7]] += 1

        # if there was a foul drawn which led to FTs, count those points
        if (data[index+1][2]) == "foul" and ("Free Throw" in data[index+2][4]):
            if "Free Throw" in data[index+2][4]:
                points[x[7]] += int(data[index+2][6])
            if ("Free Throw" in data[index+3][4]) and (data[index+3][3] == data[index+2][3]):
                points[x[7]] += int(data[index+3][6])
            if ("Free Throw" in data[index+4][4]) and (data[index+4][3] == data[index+3][3]):
                points[x[7]] += int(data[index+4][6])

        # otherwise just count the points from the ensuing play
        else:
            if data[index+1][6] != '':
                points[x[7]] += int(data[index+1][6])
            else:
                points[x[7]] += 0

boarder_arr = []
for p in boarder_poss:
    boarder_arr.append((p, float(points[p])/boarder_poss[p]))
boarder_arr.sort(key=lambda tup: tup[1], reverse=True)

# Prep results for output
print ""
print "Points off Players' OREBs"
output_framer = []
r = 1
for i, rating in enumerate(boarder_arr):
    name = "{}".format(rating[0])
    # filtering out low usage
    if (name in boarder_poss) and (boarder_poss[name] > 75):
        output_framer.append([r, name, "{}".format(rating[1])])
        print [r, "{}".format(rating[0]), "{}".format(rating[1])]
        r += 1


######################################################
# 3) Which players' OREBS led to most points? -Player
######################################################
boarder_poss = {}
points = {}
index = 1
for x in data[2:-1]:
    index += 1
    away = x[0]
    home = x[1]

    if x[4] == "rebound offensive":

        # count possessions created by offensive rebounds
        if x[3] not in boarder_poss:
            boarder_poss[x[3]] = 1
            points[x[3]] = 0
        if x[3] in boarder_poss:
            boarder_poss[x[3]] += 1

        # if there was a foul drawn which led to FTs, count those points
        if (data[index+1][2]) == "foul" and ("Free Throw" in data[index+2][4]):
            if "Free Throw" in data[index+2][4]:
                points[x[3]] += int(data[index+2][6])
            if ("Free Throw" in data[index+3][4]) and (data[index+3][3] == data[index+2][3]):
                points[x[3]] += int(data[index+3][6])
            if ("Free Throw" in data[index+4][4]) and (data[index+4][3] == data[index+3][3]):
                points[x[3]] += int(data[index+4][6])

        # otherwise just count the points from the ensuing play
        else:
            if data[index+1][6] != '':
                points[x[3]] += int(data[index+1][6])
            else:
                points[x[3]] += 0

boarder_arr = []
for p in boarder_poss:
    boarder_arr.append((p, float(points[p])/boarder_poss[p]))
boarder_arr.sort(key=lambda tup: tup[1], reverse=True)

# Prep results for output
print ""
print "Points off Players' OREBs"
output_framer = []
r = 1
for i, rating in enumerate(boarder_arr):
    name = "{}".format(rating[0])
    # filtering out low usage
    if (name in boarder_poss) and (boarder_poss[name] > 75):
        output_framer.append([r, name, "{}".format(rating[1])])
        print [r, "{}".format(rating[0]), "{}".format(rating[1])]
        r += 1

output_df = pd.DataFrame(output_framer, columns=['Rank', 'Player', 'PPP off OREB'])
output_df.to_csv("PPPoffPlayerOREBs.csv")


#######################################
# 4) Who d-boarded the most FT misses?
#######################################
boarders = {}
fts = {}
index = 1
for x in data[2:-1]:
    index += 1
    away = x[0]
    home = x[1]

    if ("Free Throw" in x[4]) and ((data[index+1][4] == "rebound defensive") or (data[index+1][4] == "rebound offensive")):
        # add missed ft events that are DREB opportunities seen by each player
        if x[3] in home:
            for n in away:
                if n not in fts:
                    fts[n] = 1
                if n in fts:
                    fts[n] += 1
        if x[3] in away:
            for n in home:
                if n not in fts:
                    fts[n] = 1
                if n in fts:
                    fts[n] += 1

    if ("Free Throw" in x[4]) and (data[index+1][4] == "rebound defensive"):
        # now add the boards from each player
        if data[index+1][3] not in boarders:
            boarders[data[index+1][3]] = 1
        if data[index+1][3] in boarders:
            boarders[data[index+1][3]] += 1

boarder_arr = []
for p in boarders:
    boarder_arr.append((p, float(boarders[p])/fts[p]))
boarder_arr.sort(key=lambda tup: tup[1], reverse=True)

# Prep results for output
print ""
print len(boarder_arr)
print "Defensive Boarding a missed FT"
output_framer = []
r = 1
for i, rating in enumerate(boarder_arr):
    name = "{}".format(rating[0])
    # filtering out low usage
    if (name in fts) and (fts[name] > 75):
        output_framer.append([r, name, "{}".format(rating[1])])
        print [r, "{}".format(rating[0]), "{}".format(rating[1])]
        r += 1

#######################################
# 5) Who o-boarded the most FT misses?
#######################################
boarders = {}
fts = {}
index = 1
for x in data[2:-1]:
    index += 1
    away = x[0]
    home = x[1]

    if ("Free Throw" in x[4]) and ((data[index+1][4] == "rebound defensive") or (data[index+1][4] == "rebound offensive")):
        # add missed ft events that are OREB opportunities seen by each player
        if x[3] in away:
            for n in away:
                if n not in fts:
                    fts[n] = 1
                if n in fts:
                    fts[n] += 1
        if x[3] in home:
            for n in home:
                if n not in fts:
                    fts[n] = 1
                if n in fts:
                    fts[n] += 1

    if ("Free Throw" in x[4]) and (data[index+1][4] == "rebound offensive"):
        # now add the boards from each player
        if data[index+1][3] not in boarders:
            boarders[data[index+1][3]] = 1
        if data[index+1][3] in boarders:
            boarders[data[index+1][3]] += 1

boarder_arr = []
for p in boarders:
    boarder_arr.append((p, float(boarders[p])/fts[p]))
boarder_arr.sort(key=lambda tup: tup[1], reverse=True)

# Prep results for output
print ""
print len(boarder_arr)
print "Offensive Boarding a missed FT"
output_framer = []
r = 1
for i, rating in enumerate(boarder_arr):
    name = "{}".format(rating[0])
    # filtering out low usage
    if (name in fts) and (fts[name] > 75):
        output_framer.append([r, name, "{}".format(rating[1])])
        print [r, "{}".format(rating[0]), "{}".format(rating[1])]
        r += 1

output_df = pd.DataFrame(output_framer, columns=['Rank', 'Player', 'FT OREB%'])
output_df.to_csv("FreeThrowOREBs.csv")


##########################################
# 6) Whose FT misses were O-boarded most?
##########################################
boarders = {}
fts = {}
index = 1
for x in data[2:-1]:
    index += 1
    away = x[0]
    home = x[1]

    if ("Free Throw" in x[4]) and ((data[index+1][4] == "rebound defensive") or (data[index+1][4] == "rebound offensive")):
        # add missed ft events produced by each player
        if x[7] not in fts:
            fts[x[7]] = 1
        if x[7] in fts:
            fts[x[7]] += 1

    if ("Free Throw" in x[4]) and (data[index+1][4] == "rebound offensive"):
        # now add the boards off each player
        if x[7] not in boarders:
            boarders[x[7]] = 1
        if x[7] in boarders:
            boarders[x[7]] += 1

boarder_arr = []
for p in boarders:
    boarder_arr.append((p, float(boarders[p])/fts[p]))
boarder_arr.sort(key=lambda tup: tup[1], reverse=True)

# Prep results for output
print ""
print len(boarder_arr)
print "Missed FT leading to OREBs"
output_framer = []
r = 1
for i, rating in enumerate(boarder_arr):
    name = "{}".format(rating[0])
    # filtering out low usage
    if (name in fts) and (fts[name] > 50):
        output_framer.append([r, name, "{}".format(rating[1])])
        print [r, "{}".format(rating[0]), "{}".format(rating[1])]
        r += 1


