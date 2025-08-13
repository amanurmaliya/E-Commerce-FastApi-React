import React, { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { adminListProducts, adminAddProduct, adminUpdateProduct, adminDeleteProduct } from '../../api/products'

const empty = { name: '', price: '', description: '', stock: '', image_url: '', category: '', rating: '' }

export default function ProductsAdminPage() {
  const qc = useQueryClient()
  const { data, isLoading, isError } = useQuery({ queryKey: ['adminProducts'], queryFn: adminListProducts })
  const [form, setForm] = useState(empty)

  const addMut = useMutation({
    mutationFn: () => {
      const payload = { ...form, price: Number(form.price), stock: Number(form.stock), rating: Number(form.rating || 0) }
      return adminAddProduct(payload)
    },
    onSuccess: () => {
      setForm(empty)
      qc.invalidateQueries({ queryKey: ['adminProducts'] })
    }
  })

  const updateMut = useMutation({
    mutationFn: ({ id, changes }) => adminUpdateProduct(id, changes),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['adminProducts'] })
  })

  const deleteMut = useMutation({
    mutationFn: (id) => adminDeleteProduct(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['adminProducts'] })
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div style={{ color: 'red' }}>Error loading products (need admin token)</div>

  return (
    <div>
      <h3>Products</h3>
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 12 }}>
        <input placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
        <input placeholder="Price" type="number" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} />
        <input placeholder="Stock" type="number" value={form.stock} onChange={(e) => setForm({ ...form, stock: e.target.value })} />
        <input placeholder="Image URL" value={form.image_url} onChange={(e) => setForm({ ...form, image_url: e.target.value })} />
        <input placeholder="Category" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} />
        <input placeholder="Rating" type="number" value={form.rating} onChange={(e) => setForm({ ...form, rating: e.target.value })} />
        <input placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
        <button onClick={() => addMut.mutate()}>Add Product</button>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Category</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {data?.map((p) => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.name}</td>
              <td>{p.price}</td>
              <td>{p.stock}</td>
              <td>{p.category}</td>
              <td>
                <button onClick={() => updateMut.mutate({ id: p.id, changes: { price: p.price + 1 } })}>+1$</button>
                <button onClick={() => deleteMut.mutate(p.id)} style={{ marginLeft: 8 }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

