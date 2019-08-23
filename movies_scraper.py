from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_search_results(movie_title):
    # Creates an instance of Chrome and makes the request.
    driver = webdriver.Chrome()
    driver.get("https://www.rottentomatoes.com/")

    # Searches for the search bar and enters the user's input.
    search_form = driver.find_element_by_class_name("form-control")
    search_form.send_keys(movie_title)
    button = driver.find_element_by_id("fullscreen-search-desktop-search-btn")
    button.click()

    # Parses the result of the search.
    results_html_soup = BeautifulSoup(driver.page_source, features="html.parser")
    movies_section = results_html_soup.find("section", id="movieSection")
    results_list = movies_section.find_all("li", class_="bottom_divider clearfix")

    # Stores the results in a dictionary for use later.
    movies_dictionary = {}
    for result in results_list:
        result_details = result.find("div", class_="details")
        movie_name = result_details.a.text.strip()
        movie_year = result_details.find("span", class_="movie_year")
        if movie_year == None:
            movie_year == ""
            movie_name_and_year = movie_name
        else:
            movie_year = movie_year.text.strip()
            movie_name_and_year = movie_name + " " + movie_year

        movie_slug = result_details.a['href']
        movies_dictionary[movie_name_and_year] = movie_slug

    driver.quit()
    return movies_dictionary

def get_movie_info(movie_slug):
    url = "https://www.rottentomatoes.com{}".format(movie_slug)

    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Extracts relevant data from the movie page
    movie_synopsis = html_soup.find("div", id="movieSynopsis").text.strip()

    movie_info_div = html_soup.find("div", class_="mop-ratings-wrap score_panel js-mop-ratings-wrap")

    title = movie_info_div.h1.text.strip()
    consensus = movie_info_div.p.text.strip()

    tomato_ratings_div = movie_info_div.find("div", class_="mop-ratings-wrap__half")
    tomato_meter = tomato_ratings_div.find("span", class_="mop-ratings-wrap__percentage")

    if tomato_meter == None:
        tomato_meter = "No reviews available"
        tomato_total_count = "N.A"
    else:
        tomato_meter = tomato_meter.text.strip()
        tomato_total_count = tomato_ratings_div.small.text.strip()

    audience_ratings_div = movie_info_div.find("div", class_="mop-ratings-wrap__half audience-score")
    audience_score = audience_ratings_div.find("span", class_="mop-ratings-wrap__percentage")

    if audience_score == None:
        audience_score = "Not available"
        audience_verified_ratings = "N.A"
    else:
        audience_score = audience_score.text.strip()
        audience_verified_ratings = audience_ratings_div.strong.text[17:].strip()
    
    info_dictionary = {}
    info_dictionary["url"] = url
    info_dictionary["title"] = title
    info_dictionary["movie_synopsis"] = movie_synopsis
    info_dictionary["consensus"] = consensus
    info_dictionary["tomato_meter"] = tomato_meter
    info_dictionary["tomato_total_count"] = tomato_total_count
    info_dictionary["audience_score"] = audience_score
    info_dictionary["audience_verified_ratings"] = audience_verified_ratings

    return info_dictionary

# def main():
#     movie_title = input("Enter Movie Name: ")
#     movies_dictionary = get_search_results(movie_title)

# main()