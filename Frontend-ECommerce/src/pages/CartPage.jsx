import React, { useMemo } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getCart, updateCartItem, removeCartItem } from '../api/cart'
import { useAuth } from '../context/AuthContext'
import { formatPrice } from '../utils/format'
import { useNavigate } from 'react-router-dom'

export default function CartPage() {
  const { userId } = useAuth()
  const qc = useQueryClient()
  const navigate = useNavigate()
  const { data, isLoading, isError } = useQuery({ queryKey: ['cart', userId], queryFn: () => getCart(userId), enabled: !!userId })

  const updateMut = useMutation({
    mutationFn: ({ product_id, quantity }) => updateCartItem(userId, { product_id, quantity }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['cart', userId] })
  })
  const removeMut = useMutation({
    mutationFn: ({ product_id }) => removeCartItem(userId, product_id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['cart', userId] })
  })

  const computedTotal = useMemo(() => {
    return (data?.items || []).reduce((sum, i) => sum + (i.price * i.quantity), 0)
  }, [data])

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div style={{ color: 'red' }}>Error loading cart</div>

  return (
    <div>
      <h2>Your Cart</h2>
      {data.items?.length === 0 && <div>Cart is empty</div>}
      {data.items?.map((item) => (
        <div key={item.product_id} style={{ display: 'flex', alignItems: 'center', gap: 8, borderBottom: '1px solid #eee', padding: '8px 0' }}>
          <div style={{ flex: 1 }}>{item.name}</div>
          <div>{formatPrice(item.price)}</div>
          <input type="number" min={1} value={item.quantity} onChange={(e) => updateMut.mutate({ product_id: item.product_id, quantity: Number(e.target.value) })} style={{ width: 80 }} />
          <div>{formatPrice(item.subtotal)}</div>
          <button onClick={() => removeMut.mutate({ product_id: item.product_id })}>Remove</button>
        </div>
      ))}
      <div style={{ marginTop: 12 }}>
        <div>Computed total: {formatPrice(computedTotal)}</div>
        <button style={{ marginTop: 12 }} onClick={() => navigate('/checkout')} disabled={data.items.length === 0}>Proceed to Checkout</button>
      </div>
    </div>
  )
}