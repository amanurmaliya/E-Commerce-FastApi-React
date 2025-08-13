import React, { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { fetchProductById } from '../api/products'
import { addToCart } from '../api/cart'
import { useAuth } from '../context/AuthContext'
import { formatPrice } from '../utils/format'

export default function ProductDetailPage() {
  const { id } = useParams()
  const { data, isLoading } = useQuery({ queryKey: ['product', id], queryFn: () => fetchProductById(id) })
  const [quantity, setQuantity] = useState(1)
  const { userId } = useAuth()
  const addMut = useMutation({ mutationFn: () => addToCart(userId, { product_id: id, quantity: Number(quantity) }) })

  if (isLoading) return <div>Loading...</div>

  const p = data
  return (
    <div>
      <h2>{p.name}</h2>
      {p.image_url && <img src={p.image_url} alt={p.name} style={{ maxWidth: 420, borderRadius: 8 }} />}
      <div>{formatPrice(p.price)}</div>
      <div>Rating: {p.rating ?? 0}</div>
      <div>Category: {p.category || '-'}</div>
      <p>{p.description}</p>
      <div>Stock: {p.stock}</div>
      <div style={{ marginTop: 8 }}>
        <input type="number" min={1} value={quantity} onChange={(e) => setQuantity(e.target.value)} style={{ width: 80 }} />
        <button onClick={() => addMut.mutate()} disabled={addMut.isPending} style={{ marginLeft: 8 }}>Add to cart</button>
        {addMut.isSuccess && <span style={{ marginLeft: 8, color: 'green' }}>Added</span>}
      </div>
    </div>
  )
}

