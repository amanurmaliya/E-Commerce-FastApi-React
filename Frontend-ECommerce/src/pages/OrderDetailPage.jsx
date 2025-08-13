import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getOrderById } from '../api/orders'

export default function OrderDetailPage() {
  const { id } = useParams()
  const { data, isLoading, isError } = useQuery({ queryKey: ['order', id], queryFn: () => getOrderById(id) })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div style={{ color: 'red' }}>Error loading order</div>

  const o = data
  return (
    <div>
      <h2>Order {o.id}</h2>
      <div>Status: {o.status || 'Pending'}</div>
      <div>User: {o.user_id}</div>
      <div>Shipping: {o.shipping_address}</div>
      <div>Total: {o.total}</div>
      <div>Products: {Array.isArray(o.products) ? o.products.join(', ') : ''}</div>
      <div>Created: {o.created_at}</div>
    </div>
  )
}

