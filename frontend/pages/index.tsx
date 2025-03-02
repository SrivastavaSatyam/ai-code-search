import { useState, ChangeEvent } from 'react'
import Head from 'next/head'
import type { NextPage } from 'next'

interface SearchResult {
  id: string;
  code: string;
  // Add other result fields as needed
}

const Home: NextPage = () => {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])

  const handleSearch = async () => {
    // TODO: Implement search functionality
  }

  const handleQueryChange = (e: ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value)
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>AI Code Search</title>
        <meta name="description" content="Search code using AI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">
          AI Code Search
        </h1>
        
        <div className="max-w-2xl mx-auto">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={handleQueryChange}
              className="flex-1 p-2 border rounded"
              placeholder="Search for code..."
            />
            <button
              onClick={handleSearch}
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              Search
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Home 