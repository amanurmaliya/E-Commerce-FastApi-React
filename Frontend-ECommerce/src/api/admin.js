import api from './axios'

export const adminListUsers = async () => {
  const res = await api.get('/admin/users')
  return res.data
}

export const adminDeleteUser = async (userId) => {
  const res = await api.delete(`/admin/users/${userId}`)
  return res.data
}

export const adminDeleteOrder = async (orderId) => {
  const res = await api.delete(`/admin/orders/${orderId}`)
  return res.data
}

