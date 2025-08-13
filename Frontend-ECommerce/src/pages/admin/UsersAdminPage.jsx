import React from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { adminListUsers, adminDeleteUser } from '../../api/admin'

export default function UsersAdminPage() {
  const qc = useQueryClient()
  const { data, isLoading, isError } = useQuery({ queryKey: ['adminUsers'], queryFn: adminListUsers })

  const delMut = useMutation({
    mutationFn: (id) => adminDeleteUser(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['adminUsers'] })
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div style={{ color: 'red' }}>Error loading users (need admin token)</div>

  return (
    <div>
      <h3>Users</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {data?.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.name}</td>
              <td>{u.email}</td>
              <td>{u.role}</td>
              <td><button onClick={() => delMut.mutate(u.id)}>Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

