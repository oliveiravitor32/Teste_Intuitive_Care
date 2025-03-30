<script setup lang="ts">
import type { IOperator } from '@/interfaces/operator.interface'
import { computed } from 'vue'

const props = defineProps<{
  results: IOperator[]
  isEmpty: boolean
  isLoading: boolean
}>()

const formatText = (text: string | null | undefined, maxLength = 50): string => {
  if (!text) return '-'
  return text.toLowerCase().length > maxLength
    ? text[0] + text.substring(1, maxLength).toLowerCase().trim() + '...'
    : text[0] + text.substring(1).toLowerCase().trim()
}
const formatDate = (text: string | null | undefined): string => {
  if (!text) return '-'
  const date = new Date(text)
  return date.toLocaleDateString('pt-BR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

// Pre-format data to avoid recalculating in the template
const formattedOperators = computed(() =>
  props.results.map((operator) => ({
    ...operator,
    formattedRegistro: formatText(operator.registro_ans),
    formattedRazaoSocial: formatText(operator.razao_social),
    formattedNomeFantasia: formatText(operator.nome_fantasia),
    formattedModalidade: formatText(operator.modalidade),
    formattedCidade: formatText(operator.cidade),
    formattedData: formatDate(operator.data_registro_ans),
  })),
)
</script>
<template>
  <tbody>
    <tr
      class="h-12 hover:cursor-pointer py-2 text-center items-center text-xs hover:bg-neutral-300 grid grid-cols-6 gap-2 border-b-1 border-gray-300"
      v-for="(item, index) in formattedOperators"
      :key="item.formattedRegistro || index"
      tabindex="0"
    >
      <td>{{ item.formattedRegistro }}</td>
      <td>{{ item.formattedRazaoSocial }}</td>
      <td>{{ item.formattedNomeFantasia }}</td>
      <td>{{ item.formattedModalidade }}</td>
      <td>{{ item.formattedCidade }}</td>
      <td>{{ item.formattedData }}</td>
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
