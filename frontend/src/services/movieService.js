import api from './api'

export const movieService = {
  getMovies: (page = 1, pageSize = 20) => 
    api.get(`/movies?page=${page}&page_size=${pageSize}`),
  getMovie: (id) => api.get(`/movies/${id}`),
  getMovieRatings: (id) => api.get(`/movies/${id}/ratings`),
  getMovieComments: (id, page = 1, pageSize = 20) => 
    api.get(`/movies/${id}/comments?page=${page}&page_size=${pageSize}`)
}
