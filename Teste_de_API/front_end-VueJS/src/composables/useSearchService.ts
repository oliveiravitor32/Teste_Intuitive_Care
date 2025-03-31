import { computed, ref, watch } from 'vue'

import type { IOperator } from '@/interfaces/operator.interface'
import type { ISearchParams } from '@/interfaces/search-params.interface'
import { searchService } from '@/services/search.service'
import debounce from 'lodash/debounce'

export function useSearchService() {
  // State
  const searchParams = ref<ISearchParams>({
    query: '',
    category: 'registro_ans',
  })
  const results = ref<IOperator[]>([])
  const isLoading = ref<boolean>(false)
  const error = ref<Error | null>(null)

  // Computed
  const hasResults = computed(() => results.value.length > 0)
  const isEmpty = computed(() => !isLoading.value && !hasResults.value)

  // Search function
  const performSearch = async () => {
    try {
      isLoading.value = true
      error.value = null

      const response = await searchService.searchOperators(searchParams.value)

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
    // Debounce the search function by 300ms when search params change
    debounce(() => performSearch(), 300),
    { deep: true },
  )

  // Method to force update
  function updateSearch(newParams: Partial<ISearchParams>) {
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
