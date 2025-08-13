export function decodeJwt(token) {
  try {
    const payload = token.split('.')[1]
    const base = payload.replace(/-/g, '+').replace(/_/g, '/')
    const padded = base.padEnd(base.length + (4 - (base.length % 4 || 4)) % 4, '=')
    const json = atob(padded)
    return JSON.parse(json)
  } catch (e) {
    return null
  }
}

