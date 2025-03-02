import { createContext, useContext, ReactNode } from 'react'
import { useSearch } from '../hooks/useSearch'

interface SearchContextType {
  results: any[];
  loading: boolean;
  error: string | null;
  search: (query: string) => Promise<void>;
}

const SearchContext = createContext<SearchContextType | null>(null)

interface SearchProviderProps {
  children: ReactNode;
}

export function SearchProvider({ children }: SearchProviderProps) {
  const searchState = useSearch()
  
  return (
    <SearchContext.Provider value={searchState}>
      {children}
    </SearchContext.Provider>
  )
}

export function useSearchContext(): SearchContextType {
  const context = useContext(SearchContext)
  if (!context) {
    throw new Error('useSearchContext must be used within a SearchProvider')
  }
  return context
} 