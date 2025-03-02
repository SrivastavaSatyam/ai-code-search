import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const searchCode = async (query: string) => {
  try {
    const response = await axios.get(`${API_URL}/search`, {
      params: { query }
    })
    return response.data
  } catch (error) {
    console.error('Error searching code:', error)
    throw error
  }
} 