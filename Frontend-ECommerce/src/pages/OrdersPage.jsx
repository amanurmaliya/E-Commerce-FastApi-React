import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import { getOrdersByUser } from '../api/orders'
import { Link } from 'react-router-dom'

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
            <Link to={`/orders/${o.id}`}>Order {o.id} - Status: {o.status || 'Pending'}</Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

