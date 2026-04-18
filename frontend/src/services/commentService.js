import api from './api'

export const commentService = {
  createComment: (movieId, content) => 
    api.post(`/movies/${movieId}/comments`, { content }),
  updateComment: (commentId, content) => 
    api.put(`/comments/${commentId}`, { content }),
  deleteComment: (commentId) => 
    api.delete(`/comments/${commentId}`)
}
