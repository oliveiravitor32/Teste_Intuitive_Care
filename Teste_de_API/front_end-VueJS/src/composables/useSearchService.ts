import { ref, computed, watch } from 'vue'

import type { ISearchParams } from '@/interfaces/search-params.interface'
import type { IOperator } from '@/interfaces/operator.interface'
import { searchService } from '@/services/search.service'

export function useSearchService() {
  // State
  const searchParams = ref<ISearchParams>({
    query: '',
    category: 'razao_social',
  })
  const results = ref<IOperator[]>([])
  const isLoading = ref<boolean>(false)
  const error = ref<Error | null>(null)

  // Computed
  const hasResults = computed(() => results.value.length > 0)
  const isEmpty = computed(() => !isLoading.value && !hasResults.value)

  // Search function with debounce
  const performSearch = async () => {
    try {
      console.log('performSearch', searchParams.value)
      isLoading.value = true
      error.value = null

      const response = await searchService.searchOperators(searchParams.value)

      console.log('response', response)

      results.value = [...response.data]
    } catch (err) {
      // error.value = err
      console.error('Error fetching search results:', err)
      results.value = []
    } finally {
      isLoading.value = false
    }
  }

  // Watch for changes to search params
  watch(
    searchParams,
    () => {
      performSearch()
    },
    { deep: true },
  )

  // Method to force update
  function updateSearch(newParams: Partial<ISearchParams>) {
    console.log('updateSearch', newParams)

    searchParams.value = {
      ...searchParams.value,
      ...newParams,
    }
  }

  return {
    // State
    searchParams,
    results,
    isLoading,
    error,

    // Computed
    hasResults,
    isEmpty,

    // Methods
    updateSearch,
  }
}
