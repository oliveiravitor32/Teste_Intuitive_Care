<script setup lang="ts">
import { useSearchService } from '@/composables/useSearchService'
import DashboardForm from './DashboardForm.vue'
import ResultsPanel from './DashboardResults.vue'

const { searchParams, results, isEmpty, isLoading } = useSearchService()
</script>

<template>
  <main class="flex max-w-5xl flex-col gap-6 border-2 border-gray-300 rounded-lg p-4">
    <section aria-labelledby="search-heading">
      <DashboardForm v-model:searchParams="searchParams"></DashboardForm>
    </section>
    <section>
      <table>
        <thead>
          <tr class="grid py-2 text-gray-600 grid-cols-6 text-sm border-b-1 border-gray-300">
            <th class="font-bold">Registro ANS</th>
            <th class="font-bold">Razão Social</th>
            <th class="font-bold">Nome Fantasia</th>
            <th class="font-bold">Modalidade</th>
            <th class="font-bold">Cidade</th>
            <th class="font-bold">Data de Registro ANS</th>
          </tr>
        </thead>
        <ResultsPanel
          v-model:results="results"
          v-model:is-empty="isEmpty"
          v-model:is-loading="isLoading"
        />
      </table>
    </section>
  </main>
</template>
