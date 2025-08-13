import React, { useMemo, useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { fetchProducts, searchProducts, filterProducts } from '../api/products'
import ProductCard from '../components/ProductCard'
import Pagination from '../components/Pagination'
import { useAuth } from '../context/AuthContext'
import { addToCart } from '../api/cart'

export default function ProductListPage() {
  const [page, setPage] = useState(1)
  const [limit] = useState(10)
  const [query, setQuery] = useState('')
  const [filters, setFilters] = useState({ category: '', min_price: '', max_price: '', min_rating: '' })

  const base = useQuery({
    queryKey: ['products', page, limit],
    queryFn: () => fetchProducts({ page, limit }),
  })

  const searchMut = useMutation({ mutationFn: (q) => searchProducts(q) })
  const filterMut = useMutation({ mutationFn: (f) => filterProducts(f) })

  const products = useMemo(() => {
    if (searchMut.data) return searchMut.data
    if (filterMut.data) return filterMut.data
    return base.data || []
  }, [base.data, searchMut.data, filterMut.data])

  const { userId } = useAuth()
  const addMut = useMutation({
    mutationFn: ({ pid }) => addToCart(userId, { product_id: pid, quantity: 1 })
  })

  const onSearch = () => {
    if (query.trim()) {
      searchMut.mutate(query.trim())
    }
  }

  const onFilter = () => {
    const payload = {}
    if (filters.category) payload.category = filters.category
    if (filters.min_price) payload.min_price = Number(filters.min_price)
    if (filters.max_price) payload.max_price = Number(filters.max_price)
    if (filters.min_rating) payload.min_rating = Number(filters.min_rating)
    filterMut.mutate(payload)
  }

  const clearOverrides = () => {
    searchMut.reset()
    filterMut.reset()
  }

  return (
    <div>
      <h2>Products</h2>
      <div style={{ display: 'flex', gap: 16, alignItems: 'end', flexWrap: 'wrap' }}>
        <div>
          <label>Search</label>
          <div>
            <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Name" />
            <button onClick={onSearch}>Search</button>
          </div>
        </div>
        <div>
          <label>Filters</label>
          <div style={{ display: 'flex', gap: 8 }}>
            <input placeholder="Category" value={filters.category} onChange={(e) => setFilters({ ...filters, category: e.target.value })} />
            <input placeholder="Min Price" type="number" value={filters.min_price} onChange={(e) => setFilters({ ...filters, min_price: e.target.value })} />
            <input placeholder="Max Price" type="number" value={filters.max_price} onChange={(e) => setFilters({ ...filters, max_price: e.target.value })} />
            <input placeholder="Min Rating" type="number" value={filters.min_rating} onChange={(e) => setFilters({ ...filters, min_rating: e.target.value })} />
            <button onClick={onFilter}>Apply</button>
            <button onClick={clearOverrides}>Clear</button>
          </div>
        </div>
        <Pagination page={page} setPage={setPage} />
      </div>

      {(base.isLoading || searchMut.isPending || filterMut.isPending) && <div>Loading...</div>}
      {(base.isError || searchMut.isError || filterMut.isError) && <div style={{ color: 'red' }}>Error loading products</div>}

      <div style={{
        marginTop: 16,
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
        gap: 16
      }}>
        {products?.map((p) => (
          <ProductCard key={p.id} product={p} onAddToCart={() => addMut.mutate({ pid: p.id })} />
        ))}
      </div>
    </div>
  )
}

