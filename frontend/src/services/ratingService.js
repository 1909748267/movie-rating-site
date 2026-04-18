import api from './api'

export const ratingService = {
  createRating: (movieId, score) => 
    api.post(`/movies/${movieId}/ratings`, { score }),
  updateRating: (movieId, score) => 
    api.put(`/movies/${movieId}/ratings`, { score }),
  getUserRating: (movieId) => 
    api.get(`/movies/${movieId}/ratings/me`)
}
