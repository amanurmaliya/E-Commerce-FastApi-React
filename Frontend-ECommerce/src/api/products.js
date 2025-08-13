import api from './axios'

export const fetchProducts = async ({ page = 1, limit = 10 } = {}) => {
  const res = await api.get(`/product-list`, { params: { page, limit } })
  return res.data
}

export const fetchProductById = async (id) => {
  const res = await api.get(`/product/${id}`)
  return res.data
}

export const searchProducts = async (query) => {
  const res = await api.post('/search-product', { query })
  return res.data
}

export const filterProducts = async (filters) => {
  const res = await api.post('/filter-products', filters)
  return res.data
}

// Admin
export const adminAddProduct = async (product) => {
  const res = await api.post('/add-product', product)
  return res.data
}

export const adminUpdateProduct = async (id, update) => {
  const res = await api.post(`/product/${id}`, update)
  return res.data
}

export const adminDeleteProduct = async (id) => {
  const res = await api.delete(`/product/${id}`)
  return res.data
}

export const adminListProducts = async () => {
  const res = await api.get('/admin/products')
  return res.data
}

