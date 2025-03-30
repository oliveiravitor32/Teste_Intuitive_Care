import type { ISearchParams } from '@/interfaces/search-params.interface'
import apiClient from './api.client'
import type { IOperatorsResponse } from '@/interfaces/operators-response.interface'

export class SearchService {
  async searchOperators(params: ISearchParams): Promise<IOperatorsResponse> {
    try {
      const { data } = await apiClient.get<IOperatorsResponse>('/operators/search', {
        params,
      })
      return data
    } catch (error) {
      // Re-throw the error to be handled by the caller
      throw error
    }
  }
}

// Create singleton instance
export const searchService = new SearchService()
