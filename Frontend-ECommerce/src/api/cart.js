import api from './axios'

export const getCart = async (userId) => {
  const res = await api.get(`/cart/${userId}`)
  return res.data
}

export const addToCart = async (userId, item) => {
  const res = await api.post(`/cart/${userId}/add`, item)
  return res.data
}

export const updateCartItem = async (userId, item) => {
  const res = await api.put(`/cart/${userId}/update`, item)
  return res.data
}

export const removeCartItem = async (userId, productId) => {
  const res = await api.delete(`/cart/${userId}/remove/${productId}`)
  return res.data
}

