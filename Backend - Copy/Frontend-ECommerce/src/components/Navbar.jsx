import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { token, setToken } = useAuth()
  const navigate = useNavigate()

  const logout = () => {
    setToken('')
    navigate('/login')
  }

  return (
    <nav style={{ display: 'flex', gap: 12, padding: 12, borderBottom: '1px solid #eee' }}>
      <Link to="/">Home</Link>
      <Link to="/cart">Cart</Link>
      <Link to="/orders">Orders</Link>
      <Link to="/admin">Admin</Link>
      <div style={{ marginLeft: 'auto' }}>
        {token ? (
          <button onClick={logout}>Logout</button>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <span style={{ margin: '0 8px' }} />
            <Link to="/register">Register</Link>
            <span style={{ margin: '0 8px' }} />
            <Link to="/admin/login">Admin Login</Link>
          </>
        )}
      </div>
    </nav>
  )
}
