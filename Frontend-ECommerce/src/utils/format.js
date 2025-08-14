export function formatPrice(value) {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'INR' }).format(value || 0)
  } catch {
    return `₹${Number(value || 0).toFixed(2)}`
  }
}

