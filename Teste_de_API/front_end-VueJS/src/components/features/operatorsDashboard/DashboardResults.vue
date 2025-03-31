<script setup lang="ts">
import {
  operatorFieldDefinitionsShortened,
  type IOperatorField,
} from '@/constants/operator-field-definitions'
import type { IOperator } from '@/interfaces/operator.interface'

const props = defineProps<{
  results: IOperator[]
  isEmpty: boolean
  isLoading: boolean
}>()

const emit = defineEmits<{
  'operator-selected': [operator: IOperator]
}>()

const onOperatorSelected = (operator: IOperator) => {
  emit('operator-selected', operator)
}

// Format a single field based on column definition
function formatField(operator: IOperator, column: IOperatorField): string {
  const value = operator[column.key as keyof IOperator]
  return column.formatter ? column.formatter(value) : String(value || '-')
}
</script>
<template>
  <tbody>
    <tr
      class="relative group grid grid-cols-5 gap-2 min-h-12 hover:cursor-pointer py-2 text-center items-center text-xs hover:bg-neutral-300 border-b-1 border-gray-300"
      v-for="(operator, index) in props.results"
      @click="onOperatorSelected(props.results[index])"
      @keydown.enter="onOperatorSelected(props.results[index])"
      :key="operator.registro_ans || index"
      tabindex="0"
      title="Clique para ver mais detalhes"
    >
      <td v-for="column in operatorFieldDefinitionsShortened" :key="column.key">
        {{ formatField(operator, column) }}
      </td>
      <i
        style="font-size: 0.6rem"
        class="absolute bg-gray-200 p-1 rounded-sm pi pi-arrow-up-right-and-arrow-down-left-from-center right-2 top-0.5 text-gray-600"
      ></i>
    </tr>
  </tbody>
  <div v-if="isEmpty" class="text-center py-3">
    <h3>Digite na barra de pesquisas para obter resultados</h3>
  </div>
  <div v-if="isLoading" class="text-center py-3">
    <i class="pi pi-spin pi-spinner" style="font-size: 2rem" aria-hidden="true"></i>
    <span class="sr-only">Carregando...</span>
  </div>
</template>
