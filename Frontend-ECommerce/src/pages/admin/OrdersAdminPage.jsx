import React, { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { adminListOrders, adminUpdateOrderStatus } from '../../api/orders'
import { adminDeleteOrder } from '../../api/admin'

export default function OrdersAdminPage() {
  const qc = useQueryClient()
  const { data, isLoading, isError } = useQuery({ queryKey: ['adminOrders'], queryFn: adminListOrders })
  const [status, setStatus] = useState('Pending')

  const statusMut = useMutation({
    mutationFn: ({ id, status }) => adminUpdateOrderStatus(id, status),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['adminOrders'] })
  })

  const delMut = useMutation({
    mutationFn: (id) => adminDeleteOrder(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['adminOrders'] })
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div style={{ color: 'red' }}>Error loading orders (need admin token)</div>

  return (
    <div>
      <h3>Orders</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>User</th>
            <th>Status</th>
            <th>Total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {data?.map((o) => (
            <tr key={o.id}>
              <td>{o.id}</td>
              <td>{o.user_id}</td>
              <td>{o.status}</td>
              <td>{o.total}</td>
              <td>
                <select value={status} onChange={(e) => setStatus(e.target.value)}>
                  {['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled'].map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
                <button onClick={() => statusMut.mutate({ id: o.id, status })}>Update</button>
                <button onClick={() => delMut.mutate(o.id)} style={{ marginLeft: 8 }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

