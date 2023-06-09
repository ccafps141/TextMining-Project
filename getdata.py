import os


def get_all_movies():
    folder_path = './wordclouds' # path
    file_list = []
    for file_name in os.listdir(folder_path):
        file_name_without_ext = os.path.splitext(file_name)[0]
        file_list.append(file_name_without_ext)

    return (file_list)


if __name__ == "__main__":

    # output the movies we predefined
    movies = get_all_movies()
    with open("movies_for_prompt.txt", "w", encoding="utf-8") as file:
        file.write("、".join(movies))

