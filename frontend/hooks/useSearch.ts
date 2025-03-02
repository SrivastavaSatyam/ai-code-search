import { useState } from 'react'
import { searchCode } from '../utils/api'

interface SearchResult {
  id: string;
  code: string;
  // Add other result fields as needed
}

export function useSearch() {
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const search = async (query: string) => {
    try {
      setLoading(true)
      setError(null)
      const data = await searchCode(query)
      setResults(data.results)
    } catch (err) {
      setError('Failed to search code')
    } finally {
      setLoading(false)
    }
  }

  return { results, loading, error, search }
} 