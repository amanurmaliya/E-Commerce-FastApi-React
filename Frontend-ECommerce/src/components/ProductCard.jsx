import React from 'react'
import { Link } from 'react-router-dom'
import { formatPrice } from '../utils/format'

export default function ProductCard({ product, onAddToCart }) {
  return (
    <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 12 }}>
      {product.image_url && (
        <img src={product.image_url} alt={product.name} style={{ width: '100%', height: 160, objectFit: 'cover', borderRadius: 8 }} />
      )}
      <h4>{product.name}</h4>
      <div>{formatPrice(product.price)}</div>
      <div>Rating: {product.rating ?? 0}</div>
      <div style={{ marginTop: 8, display: 'flex', gap: 8 }}>
        <Link to={`/product/${product.id}`}>View</Link>
        {onAddToCart && (
          <button onClick={() => onAddToCart(product)}>Add to cart</button>
        )}
      </div>
    </div>
  )
}

