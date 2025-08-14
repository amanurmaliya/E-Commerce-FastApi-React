import React, { useMemo, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { adminListOrders, adminUpdateOrderStatus } from '../../api/orders'
import { adminDeleteOrder, adminListUsers } from '../../api/admin'
import { adminListProducts } from '../../api/products'

export default function OrdersAdminPage() {
  const qc = useQueryClient()
  const ordersQ = useQuery({ queryKey: ['adminOrders'], queryFn: adminListOrders })
  const usersQ = useQuery({ queryKey: ['adminUsers'], queryFn: adminListUsers })
  const productsQ = useQuery({ queryKey: ['adminProducts'], queryFn: adminListProducts })
  const [statusById, setStatusById] = useState({})

  const statusMut = useMutation({
    mutationFn: ({ id, status }) => adminUpdateOrderStatus(id, status),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['adminOrders'] })
  })

  const delMut = useMutation({
    mutationFn: (id) => adminDeleteOrder(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['adminOrders'] })
  })

  const userIdToName = useMemo(() => {
    const map = {}
    ;(usersQ.data || []).forEach((u) => { map[u.id] = u.name })
    return map
  }, [usersQ.data])

  const productIdToName = useMemo(() => {
    const map = {}
    ;(productsQ.data || []).forEach((p) => { map[p.id] = p.name })
    return map
  }, [productsQ.data])

  const getStatusValue = (o) => statusById[o.id] ?? o.status ?? 'Pending'

  if (ordersQ.isLoading || usersQ.isLoading || productsQ.isLoading) return <div>Loading...</div>
  if (ordersQ.isError) return <div style={{ color: 'red' }}>Error loading orders (need admin token)</div>

  return (
    <div>
      <h3>Orders</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>User</th>
            <th>Products</th>
            <th>Status</th>
            <th>Total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {ordersQ.data?.map((o) => (
            <tr key={o.id}>
              <td>{o.id}</td>
              <td>{userIdToName[o.user_id] || o.user_id}</td>
              <td>{Array.isArray(o.products) ? o.products.map(pid => productIdToName[pid] || pid).join(', ') : ''}</td>
              <td>{o.status}</td>
              <td>{o.total}</td>
              <td>
                <select
                  value={getStatusValue(o)}
                  onChange={(e) => setStatusById((prev) => ({ ...prev, [o.id]: e.target.value }))}
                >
                  {['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled'].map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
                <button onClick={() => statusMut.mutate({ id: o.id, status: getStatusValue(o) })}>Update</button>
                <button onClick={() => delMut.mutate(o.id)} style={{ marginLeft: 8 }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

