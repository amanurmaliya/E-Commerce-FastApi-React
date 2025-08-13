import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { decodeJwt } from '../utils/jwt'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token') || '')
  const [userId, setUserId] = useState(() => localStorage.getItem('userId') || '')

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
      const payload = decodeJwt(token)
      const uid = payload?.user_id || payload?.userId || ''
      setUserId(uid)
      if (uid) localStorage.setItem('userId', uid)
    } else {
      localStorage.removeItem('token')
      setUserId('')
      localStorage.removeItem('userId')
    }
  }, [token])

  const value = useMemo(() => ({ token, setToken, userId }), [token, userId])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

