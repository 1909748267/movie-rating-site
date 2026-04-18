import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'
import { auth } from './utils/auth'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'

function Header() {
  const navigate = useNavigate()
  const user = auth.getUser()
  const isAuthenticated = auth.isAuthenticated()

  const handleLogout = () => {
    auth.removeToken()
    auth.removeUser()
    navigate('/')
  }

  return (
    <header style={{ 
      backgroundColor: '#333', 
      color: 'white', 
      padding: '10px 20px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '20px', fontWeight: 'bold' }}>
        电影评分网站
      </Link>
      <nav>
        {isAuthenticated ? (
          <>
            <span style={{ marginRight: '15px' }}>欢迎, {user?.username}</span>
            <button 
              onClick={handleLogout}
              style={{ 
                backgroundColor: 'transparent', 
                color: 'white', 
                border: '1px solid white',
                padding: '5px 15px',
                cursor: 'pointer'
              }}
            >
              登出
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: 'white', marginRight: '15px', textDecoration: 'none' }}>登录</Link>
            <Link to="/register" style={{ color: 'white', textDecoration: 'none' }}>注册</Link>
          </>
        )}
      </nav>
    </header>
  )
}

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
