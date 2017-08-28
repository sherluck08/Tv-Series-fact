"""
Tv Series trivia 0.1

Know interesting fact about your favourite Tv series

"""

from bs4 import BeautifulSoup
import requests



def menu():
    print("\n")
    print("+--------------------------------+")
    print("+--------------------------------+")
    print("+-------Tv Series Trivia---------+")
    print("+--------------------------------+")
    print("+--------------------------------+")

# This function ask the user to enter the name of the movie they want to search_movie
# and when it found it, it goes to the movie page
def search():

    running = True
    while running:

        menu()
        print('Enter the name of the movie (Enter to quit): ')
        search_movie = input('>>> ')
        if search_movie != '':
            try:
                r = requests.get('http://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=all'.format(search_movie))
                try:
                    html = r.content
                    soup = BeautifulSoup(html, 'html.parser')
                    goto_movie_page = soup.find('td', {'class':'result_text'}).a
                    href = goto_movie_page.get('href')
                    movie_page_link = 'http://www.imdb.com' + href
                    sub_moviepage_url = movie_page_link[:-17]
                    print('The link to the search movie {} is {}'.format(search_movie, movie_page_link))
                    find_trivia_link_on_movie_page(sub_moviepage_url, movie_page_link)
                except AttributeError:
                    print("[+] {} not found! Try searching for another movie ".format(search_movie))

            except requests.exceptions.ConnectionError:
                print("[+] Error: Network is down..")

        else:
            print('[+] Quiting...')
            running = False


#This function below get the link of the "trivia " on the movie page
def find_trivia_link_on_movie_page(movie_sub_url, trivia_link):

    req = requests.get(trivia_link)
    soup = BeautifulSoup(req.content, 'html.parser')
    go_to_trivia_page = soup.find('a', {'class':'nobr'})
    href = go_to_trivia_page.get('href')
    full_trivia_page_url = movie_sub_url + href
    trivia(full_trivia_page_url)

#This function below fetch the trivia text
def trivia(url):

    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    trivia_text = soup.find_all('div', {'class':'sodatext'})
    for text in trivia_text:
        print("-" * 58)
        print(text.get_text())
    print("")
    print('[+] This is the end of the trivia')





if __name__ == '__main__':
    search()
