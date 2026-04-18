import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { movieService } from '../services/movieService'
import { auth } from '../utils/auth'

function Home() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    loadMovies()
  }, [])

  const loadMovies = async () => {
    try {
      setLoading(true)
      const response = await movieService.getMovies()
      if (response.code === 'SUCCESS') {
        setMovies(response.data.movies)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>加载中...</div>
  if (error) return <div>错误: {error}</div>

  return (
    <div>
      <h2>最近上映电影</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px' }}>
        {movies.map(movie => (
          <div 
            key={movie.id} 
            onClick={() => navigate(`/movie/${movie.id}`)}
            style={{ cursor: 'pointer', border: '1px solid #ddd', padding: '10px', borderRadius: '8px' }}
          >
            {movie.poster_url && (
              <img 
                src={movie.poster_url} 
                alt={movie.title} 
                style={{ width: '100%', height: '300px', objectFit: 'cover' }}
              />
            )}
            <h3>{movie.title}</h3>
            {movie.director && <p>导演: {movie.director}</p>}
            {movie.avg_score > 0 && (
              <p>评分: {movie.avg_score.toFixed(1)} ({movie.rating_count}人)</p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Home
