import requests
from datetime import datetime
import datetime


def igdb_search(search_term):
    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Authorization': 'Bearer zpeqvto2s4aizi9n5spaysn83mea4o',
        'Client-ID': 'ghorri377u2j6upf0lry6ggtgeczc8',
    }

    fields = 'id, name, platforms.name, aggregated_rating, rating_count, first_release_date, category, status, summary, cover.image_id, slug'
    platforms = '6, 18, 19, 4, 21, 5, 41, 130, 7, 2, 3, 48, 167, 12, 49, 169, 32, 29'

    query = f'search "{search_term}"; fields {fields}; where platforms = ({platforms}) & category = (0, 2, 8, 9); limit 200;'

    response = requests.post(url, headers=headers, data=query)
    
    igdb_data = response.json()

    def filter_editions(data):
        return [game for game in data if 'Edition' not in game.get('name', '')]

    def filter_cancelled(data):
        return [game for game in data if game.get('status', '') != 6]

    def filter_no_release_year(data):
        return [game for game in data if game.get('first_release_date') is not None ]

    igdb_data = filter_editions(igdb_data)
    igdb_data = filter_cancelled(igdb_data)
    igdb_data = filter_no_release_year(igdb_data)
    
    for game in igdb_data:
        release_date_timestamp = game.get('first_release_date')
        if release_date_timestamp:
            release_date = datetime.datetime.utcfromtimestamp(int(release_date_timestamp))
            game['first_release_date'] = release_date.date()

        cover_id = game.get('cover', {}).get('image_id', '')
        game['cover_id'] = cover_id
    


    sorted_data_by_rating_count = sorted(igdb_data, key=lambda x: x.get('rating_count', 0), reverse=True)
    
    return sorted_data_by_rating_count


def fetch_game_by_slug(slug):
    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Authorization': 'Bearer zpeqvto2s4aizi9n5spaysn83mea4o',
        'Client-ID': 'ghorri377u2j6upf0lry6ggtgeczc8',
    }

    fields = 'id, name, first_release_date, genres.name, platforms.name, cover.image_id, slug, summary, screenshots.image_id, involved_companies.company.name'
    platforms = '6, 18, 19, 4, 21, 5, 41, 130, 7, 2, 3, 48, 167, 12, 49, 169, 32, 29'

    query = f'fields {fields}; where slug = "{slug}";'

    response = requests.post(url, headers=headers, data=query)
    
    igdb_data = response.json()

    release_date_timestamp = igdb_data[0]['first_release_date']
    if release_date_timestamp:
        release_date = datetime.datetime.utcfromtimestamp(int(release_date_timestamp))
        igdb_data[0]['first_release_date'] = release_date.date()

    return igdb_data

def get_companies(data):
    companies_data = data[0]['involved_companies']
    companies = []

    for c in companies_data:
        company = c['company']['name']
        companies.append(company)
    
    return ', '.join(companies)

def get_genres(data):
    genres_data = data[0]['genres']
    genres = []

    for g in genres_data:
        genre = g['name']
        genres.append(genre)
    
    return genres

def get_platforms(data):
    platform_data = data[0]['platforms']
    platforms = []

    for p in platform_data:
        genre = p['name']
        platforms.append(genre)
    
    return platforms