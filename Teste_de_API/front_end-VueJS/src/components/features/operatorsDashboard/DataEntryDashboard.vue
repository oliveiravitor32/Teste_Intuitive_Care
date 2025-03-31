<script setup lang="ts">
import { useSearchService } from '@/composables/useSearchService'
import type { IOperator } from '@/interfaces/operator.interface'
import { ref, type Ref } from 'vue'
import DashboardForm from './DashboardForm.vue'
import DashboardResults from './DashboardResults.vue'
import OperatorDialog from './OperatorDialog.vue'

const { searchParams, results, isEmpty, isLoading } = useSearchService()

const showDialog: Ref<boolean> = ref(false)
const selectedOperator: Ref<IOperator | null> = ref(null)

const onOperatorSelected = (operator: IOperator) => {
  selectedOperator.value = operator
  showDialog.value = true
}
</script>

<template>
  <div>
    <span class="block text-center pb-2 text-gray-800 text-sm md:text-base"
      >Clique nos resultados para obter mais detalhes.</span
    >
    <main class="flex max-w-5xl flex-col gap-6 border-2 border-gray-300 rounded-lg p-4">
      <section aria-labelledby="search-heading">
        <DashboardForm v-model:searchParams="searchParams"></DashboardForm>
      </section>
      <section>
        <table>
          <thead>
            <tr
              class="grid py-2 text-xs md:text-sm text-gray-600 grid-cols-5 border-b-1 border-gray-300"
            >
              <th class="font-bold">Registro ANS</th>
              <th class="font-bold">Razão Social</th>
              <th class="font-bold">Modalidade</th>
              <th class="font-bold">Cidade</th>
              <th class="font-bold">Data de Registro ANS</th>
            </tr>
          </thead>
          <DashboardResults
            :results="results"
            :is-empty="isEmpty"
            :is-loading="isLoading"
            @operator-selected="onOperatorSelected"
          />
        </table>
      </section>
      <OperatorDialog :selectedOperator="selectedOperator" v-model:showDialog="showDialog" />
    </main>
  </div>
</template>
