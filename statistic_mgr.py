


watched_movie = dict() # key: user id, value: list of movies the user watched
user_input = dict() # key: user id, value: list of input the user typed


def update_movie_record(user_id, movie_title):

    if user_id not in watched_movie.keys():
        watched_movie[user_id] = []
        watched_movie[user_id].append(movie_title)
    else:
        if movie_title not in watched_movie[user_id]:
            watched_movie[user_id].append(movie_title)


def update_user_input(user_id, text):
    if user_id not in user_input:
        user_input[user_id] = []
        user_input[user_id].append(text)
    else:
        user_input[user_id].append(text)

    

# if __name__ == '__main__':
    