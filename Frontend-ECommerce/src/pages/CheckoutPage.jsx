import React, { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { getCart } from '../api/cart'
import { useAuth } from '../context/AuthContext'
import { placeOrder } from '../api/orders'
import { formatPrice } from '../utils/format'

export default function CheckoutPage() {
  const { userId } = useAuth()
  const { data } = useQuery({ queryKey: ['cart', userId], queryFn: () => getCart(userId), enabled: !!userId })
  const [address, setAddress] = useState('')
  const navigate = useNavigate()
  const qc = useQueryClient()

  const items = data?.items || []
  const total = useMemo(() => items.reduce((sum, i) => sum + (i.price * i.quantity), 0), [items])

  const onPlaceOrder = async () => {
    const products = items.flatMap((i) => Array.from({ length: i.quantity }, () => i.product_id))
    const payload = { products, total, user_id: userId, shipping_address: address }
    const res = await placeOrder(payload)
    if (res?.order_id) {
      // Backend clears the cart; invalidate local cache and navigate
      await qc.invalidateQueries({ queryKey: ['cart', userId] })
      navigate(`/orders/${res.order_id}`)
    }
  }

  return (
    <div>
      <h2>Checkout</h2>
      <div>
        <label>Shipping address</label>
        <textarea rows={3} value={address} onChange={(e) => setAddress(e.target.value)} style={{ width: '100%', maxWidth: 420 }} />
      </div>
      <div style={{ marginTop: 12 }}>
        <h3>Summary</h3>
        {items.map((i) => (
          <div key={i.product_id} style={{ display: 'flex', gap: 8 }}>
            <div style={{ flex: 1 }}>{i.name}</div>
            <div>x {i.quantity}</div>
            <div>{formatPrice(i.price * i.quantity)}</div>
          </div>
        ))}
        <div style={{ marginTop: 12, fontWeight: 'bold' }}>Total: {formatPrice(total)}</div>
      </div>
      <button style={{ marginTop: 12 }} onClick={onPlaceOrder} disabled={!address || items.length === 0}>Place order</button>
    </div>
  )
}

