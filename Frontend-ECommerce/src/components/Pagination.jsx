import React from 'react'

export default function Pagination({ page, setPage, hasNext = true }) {
  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page <= 1}>Prev</button>
      <span>Page {page}</span>
      <button onClick={() => setPage((p) => p + 1)} disabled={!hasNext}>Next</button>
    </div>
  )
}

