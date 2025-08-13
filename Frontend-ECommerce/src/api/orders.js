import api from './axios'

export const placeOrder = async (order) => {
  const res = await api.post('/orders', order)
  return res.data
}

export const getOrderById = async (id) => {
  const res = await api.get(`/orders/${id}`)
  return res.data
}

export const getOrdersByUser = async (userId) => {
  const res = await api.get(`/orders/user/${userId}`)
  return res.data
}

// Admin
export const adminListOrders = async () => {
  const res = await api.get('/orders')
  return res.data
}

export const adminUpdateOrderStatus = async (id, status) => {
  const res = await api.put(`/admin/orders/${id}/status`, null, { params: { status } })
  return res.data
}

