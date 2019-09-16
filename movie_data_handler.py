#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tmdbsimple as tmdb
from keys import API_KEY

def get_release_date(movie_id): # цифровая или физикал премьера
	release_dates = []
	tmdb.API_KEY = API_KEY
	movie = tmdb.Movies(movie_id)
	results = movie.release_dates()['results']
	for a in results:
		for b in a['release_dates']:
			if b['type'] > 3: # 4 - Digital, 5 - Physical, 6 - TV
				release_dates.append(b['release_date'].split('T')[0])

	print ('Getting release date')
	if release_dates:
		return min(release_dates)
	else:
		return 0

def get_movie_ids_by_title(title):
	movie_ids = []
	tmdb.API_KEY = API_KEY
	search = tmdb.Search()
	response = search.movie(query = title)
	for s in search.results:
		movie_ids.append({'title': s['title'], 'id': s['id'], 'release_date': s['release_date']})
	print ('Getting movie ids by title: ' + title)
	return movie_ids


if __name__ == '__main__':
	movies = get_movie_ids_by_title("x men")
	output = ['Select your movie:']
	for m in movies:
		output.append(str(movies.index(m)+1) + ') ' + m['title'] + ', премьера: ' + m['release_date'])
	# print("\n".join(output))ss
