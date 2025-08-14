import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getOrderById } from '../api/orders'
import { fetchProductById } from '../api/products'
import { useAuth } from '../context/AuthContext'
import { decodeJwt } from '../utils/jwt'

export default function OrderDetailPage() {
  const { id } = useParams()
  const { token } = useAuth()
  const orderQ = useQuery({ queryKey: ['order', id], queryFn: () => getOrderById(id) })

  const productsQ = useQuery({
    queryKey: ['orderProducts', orderQ.data?.products],
    queryFn: async () => {
      const ids = Array.isArray(orderQ.data?.products) ? orderQ.data.products : []
      const results = await Promise.all(ids.map((pid) => fetchProductById(pid).catch(() => null)))
      return results
    },
    enabled: !!orderQ.data
  })

  if (orderQ.isLoading) return <div>Loading...</div>
  if (orderQ.isError) return <div style={{ color: 'red' }}>Error loading order</div>

  const o = orderQ.data
  const email = decodeJwt(token)?.email
  const productNames = (productsQ.data || []).filter(Boolean).map((p) => p.name)

  return (
    <div>
      <h2>Order {o.id}</h2>
      <div>Status: {o.status || 'Pending'}</div>
      <div>User: {email || o.user_id}</div>
      <div>Shipping: {o.shipping_address}</div>
      <div>Total: {o.total}</div>
      <div>Products: {productNames.join(', ')}</div>
      <div>Created: {o.created_at}</div>
    </div>
  )
}

