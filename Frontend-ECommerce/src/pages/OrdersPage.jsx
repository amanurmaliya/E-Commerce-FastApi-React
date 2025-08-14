import React from 'react'
import { useQuery, useQueries } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import { getOrdersByUser } from '../api/orders'
import { Link } from 'react-router-dom'
import { fetchProductById } from '../api/products'

function OrderProductsNames({ productIds = [] }) {
  const queries = useQueries({
    queries: productIds.map((id) => ({
      queryKey: ['product', id],
      queryFn: () => fetchProductById(id),
      staleTime: 5 * 60 * 1000,
    }))
  })

  const anyLoading = queries.some((q) => q.isLoading)
  if (anyLoading) return <span>Loading products...</span>

  const names = queries.map((q) => q.data?.name || 'Unknown')
  return <span>{names.join(', ')}</span>
}

export default function OrdersPage() {
  const { userId } = useAuth()
  const { data, isLoading, isError } = useQuery({ queryKey: ['ordersByUser', userId], queryFn: () => getOrdersByUser(userId), enabled: !!userId })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div style={{ color: 'red' }}>Error loading orders</div>

  return (
    <div>
      <h2>My Orders</h2>
      {(!data || data.length === 0) && <div>No orders</div>}
      <ul>
        {data?.map((o) => (
          <li key={o.id}>
            <Link to={`/orders/${o.id}`}>
              <div>
                <div>Products: <OrderProductsNames productIds={Array.isArray(o.products) ? o.products : []} /></div>
                <div>Status: {o.status || 'Pending'}</div>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

