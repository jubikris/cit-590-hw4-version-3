# movie trivia.py
# Jubi Krishnamoorthy, Wei Chen

#use these first 2 functions to create your 2 dictionaries
import csv
def create_actors_DB(actor_file):
    '''Create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = (actorAndMovies[0]).lower()
        movies = [x.lstrip().rstrip().lower() for x in actorAndMovies[1:]]
        #movieInfo[actor] = set(movies)
        movieInfo[actor] = movies
        #should we change this, so we can further edit and append?
    f.close()
    return movieInfo

def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict[row[0].lstrip().rstrip().lower()] = [row[1], row[2]]
    return scores_dict
##########

def create_good_movies(goodmovies_file):
    '''make a dictionary from the csv file for good movies'''
    scores_dict = []
    with open(goodmovies_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict.append(row[0].lstrip().rstrip().lower())
    return scores_dict

def insert_actor_info(actor, movies, movie_Db):
    movies_list = []
    if actor.lower().rstrip().lstrip() in movie_Db:
        movies_list = movie_Db[actor]
    movies_list.extend(movies)
    movie_Db[actor] = movies_list

def insert_rating(movie, ratings, ratings_Db):
    ratings_Db[movie.lower().rstrip().lstrip()] = ratings

def delete_movie(movie, movie_Db, ratings_Db):
    del ratings_Db[movie.lower().rstrip().lstrip()]
    movies_of_all_actors = movie_Db.values()
    for movies_list in movies_of_all_actors:
        if movie in movies_list:
            movies_list.remove(movie)

def select_where_actor_is(actorName, movie_Db):
    return movie_Db[actorName.lower().rstrip().lstrip()]

def select_where_movie_is(movieName, movie_Db):
    all_actors_list = movie_Db.keys()
    actors_list = []
    for actor in all_actors_list[0:]:
        if movieName.lower().rstrip().lstrip() in movie_Db[actor]:
            actors_list.append(actor)
    return actors_list

def select_where_rating_is(targeted_rating, comparison, is_critic, ratings_Db):
    movies_with_target = []
    all_movies_list = ratings_Db.keys()
    for movie in all_movies_list:
        rating_tuple = ratings_Db[movie]
        if is_critic:
            rating = int(rating_tuple[0])
        else:
            rating = int(rating_tuple[1])
        if comparison == '=':
            if rating == targeted_rating:
                movies_with_target.append(movie)
        if comparison == '<':
            if rating < targeted_rating:
                movies_with_target.append(movie)
        if comparison == '>':
            if rating > targeted_rating:
                movies_with_target.append(movie)
    return movies_with_target
     
   
#USER QUESTION!!!!!!!!!!

def get_co_actors(actorName, moviedb):
    co_actors = []
    movies_acted = moviedb[actorName.lower().rstrip().lstrip()]
    for movie in movies_acted:
        for actor in moviedb.keys():
            if movie in moviedb[actor] and actor != actorName:
                co_actors.append(actor)
    return co_actors

def get_common_movie(actor1, actor2, moviedb):
    common_movies = []
    movies_actor1_acted = moviedb[actor1.lower().rstrip().lstrip()]
    for movie in movies_actor1_acted:
        if movie in moviedb[actor2.lower().rstrip().lstrip()]:
            common_movies.append(movie)
    return common_movies

def critics_darling(movie_Db, ratings_Db):
    actor_and_rating = {}
    actors_wid_hi_rating = []
    for actor in movie_Db.keys():
        sum_of_rating = 0.0
        no_of_movies = 0
        for movie in movie_Db[actor]:
            if movie in ratings_Db.keys():
                rating_tuple = ratings_Db[movie]
                sum_of_rating += int(rating_tuple[0])
                no_of_movies += 1
        average_rating = sum_of_rating / no_of_movies
        actor_and_rating[actor] = average_rating
    for actor in actor_and_rating.keys():
        if actor_and_rating[actor] == max(actor_and_rating.values()):
            actors_wid_hi_rating.append(actor)
    return actors_wid_hi_rating

def audience_darling(movie_Db, ratings_Db):
    '''finding the actor whose movies have the highest average rotten tomatoes rating, as per the audience.This returns a list of actors '''
    actor_and_rating={}
    actors_wid_hi_rating = []
    #select_where_actor_is(actorName, movie_Db)
    movie_Db.values()
    for actor in movie_Db.keys():
        #named i as sum_of_rating
        sum_of_rating = 0.0
        #how to deal with the error, cannot find relative rating in another db?
        for movies in movie_Db[actor]:
            sum_of_rating += 1
            if movies in ratings_Db.keys():
                rate_per_audience=ratings_Db[movies]
                #takes care of word not being in dict initially
                actor_and_rating[actor] =actor_and_rating.get(actor,0) + int(rate_per_audience[1])
        #freq[actor]=freq[actor]/float(len(movie_Db[actor]))
        actor_and_rating[actor]=actor_and_rating[actor]/sum_of_rating
        #what if not all the movies are in ratingDB
    for actor in actor_and_rating.keys():
        if actor_and_rating[actor]==max(actor_and_rating.values()):
            #return actor
            #only one return? made some changes as we have to return a list
            actors_wid_hi_rating.append(actor)
            #print audience_darling
    return actors_wid_hi_rating

def good_movies(ratings_Db):
    ''' returns the set of movies that both critics and the audience have rated above 85 (greater than equal to 85). '''
    good_movies=[]
    audience_rate1=select_where_rating_is(85, '=', False, ratings_Db)
    audience_rate2=select_where_rating_is(85, '>', False, ratings_Db)
    for movies in audience_rate2:
        audience_rate1.append(movies)
    #print audience_rate1
    #print len(audience_rate1)
    critics_rate1=select_where_rating_is(85, '=', True, ratings_Db)
    critics_rate2=select_where_rating_is(85, '>', True, ratings_Db)
    for movies in critics_rate2:
        critics_rate1.append(movies)
    #print critics_rate1
    #print len(critics_rate1)
    for movies in audience_rate1:
        if movies in critics_rate1:
            good_movies.append((movies.rstrip().lstrip()))
    #print len(good_movies)
    return good_movies
#might not be the optimal one, but this could use former constructed code
    
def get_common_actors(movie1, movie2, movies_Db):
    ''' Given a pair of movies, return a list of actors that acted in both'''
    actors_list=[]
    actors_list1=select_where_movie_is(movie1.lower().rstrip().lstrip(), movies_Db)
    actors_list2=select_where_movie_is(movie2.lower().rstrip().lstrip(), movies_Db)
    for actors in actors_list1:
        if actors in actors_list2:
            actors_list.append(actors)
    return actors_list
    #what if no common actors? return a message?

def get_bacon(actor, movieDb):
    ''' Get an actor's Bacon number'''
    actor_list=['Kevin Bacon']
    co_actors=get_co_actors('Kevin Bacon', movieDb)
    for co_actor in co_actors:
        actor_list.append(co_actor)
    actor_list=set(actor_list)
    actor_list=list(actor_list)
    co_actors_list=[]
    i=0
    #set? list?
    #print len(set(movieDb.keys()))
    #print len(actor_list)
    #print len(movieDb)
    #while len(actor_list)!=3:
    while len(actor_list)!=63:
        #caculate with the outcome, how can we get at first??
        #what if the database changes?
        i+=1
        if actor in co_actors:
            return i
            #break
        else:
            #print i
            for next_actor in co_actors:
                co_actors_next=get_co_actors(next_actor, movieDb)
                for every_actor in co_actors_next:
                    co_actors_list.append(every_actor)
                    actor_list.append(every_actor)
                #print co_actors_list
                co_actors_list=set(co_actors_list)
                co_actors_list=list(co_actors_list)
                co_actors=co_actors_list
        actor_list=set(actor_list)
        actor_list=list(actor_list)
        #print len(actor_list),'len'
        #print actor_list
    return 0

       
            
        
def main():
    actor_DB = create_actors_DB('movies.txt')
    ratings_DB = create_ratings_DB('moviescores.csv')
    good_movies_csv = create_good_movies('good_movies.csv')
    user_choice = '9'
    while user_choice == '9':
        user_choice = raw_input('''
                                press 1 to know the movies of your favorite actor
                                press 2 to know the actors acted in your favorite movie
                                press 3 to know the Actors (Co_actors) acted with your favorite actor
                                press 4 to know about the movie in which two of your favorite actors played a role
                                press 5 if you wanna now who is the critics darling of the year
                                press 6 if you wanna now who is the audience darling of the year
                                press 7 to know the top rated movies by both audience and critics
                                press 8 to know about the actors who acted in two of your favorite movies''')
        if user_choice == '1':
            actor = raw_input('enter the actor\'s name')
            movie = select_where_actor_is(actor, actor_DB)
            print 'The movies your favorite actor acted are', movie

        elif user_choice == '2':
            movie = raw_input('enter the Movie\'s name')
            actor = select_where_movie_is(movie, actor_DB)
            print 'The actor\'s acted in your favorite  movie are', actor

        elif user_choice == '3':
            actor = raw_input('enter the actor\'s name')
            print 'The Co_actors are', get_co_actors(actor, actor_DB)

        elif user_choice == '4':
            actor1 = raw_input('enter the actor 1 name')
            actor2 = raw_input('enter the actor 2 name')
            print 'The movies in which both', actor1, 'and', actor2, 'are', get_common_movie(actor1, actor2, actor_DB)

        elif user_choice == '5':
            print 'The critics darling is', critics_darling(actor_DB, ratings_DB)

        elif user_choice == '6':
            print 'The Audience darling is', audience_darling(actor_DB, ratings_DB)

        elif user_choice == '7':
            print 'the top rated movies by both audience and critics are\n'
            top_rated_movies = good_movies(ratings_DB)
            length = len(top_rated_movies) 
            print length
            for i in range(0,length):
                print top_rated_movies[i]

        elif user_choice == '8':
            movie1 = raw_input('enter the movie 1 name')
            movie2 = raw_input('enter the movie 2 name')
            print 'The actors who acted in both', movie1, 'and', movie2,  'are', get_common_actors(movie1, movie2, actor_DB)
        
        else:
            print 'the choice you made is incorrect'

        print 'if you wanna know more information press 9 else type "quit"'
        user_choice = raw_input()
        while user_choice != '9' and user_choice != 'quit':
            print 'please enter 9 to continue or quit'
            user_choice = raw_input()

    




        
    
    
        
        
    
if __name__ == '__main__':
    main()




            

