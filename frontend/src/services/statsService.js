import api from './api'

export const statsService = {
  getStats: () => api.get('/stats')
}
