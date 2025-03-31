<script setup lang="ts">
import type { ISearchParams } from '@/interfaces/search-params.interface'

const SEARCH_CATEGORIES = [
  { value: 'razao_social', label: 'Razão Social' },
  { value: 'nome_fantasia', label: 'Nome Fantasia' },
]

const props = defineProps<{
  searchParams: ISearchParams
}>()

const emit = defineEmits<{
  'update:searchParams': [ISearchParams]
}>()

// Forward update events
function updateCategory(value: string) {
  emit('update:searchParams', { ...props.searchParams, category: value })
}

function updateQuery(value: string) {
  emit('update:searchParams', { ...props.searchParams, query: value })
}
</script>

<template>
  <form @submit.prevent class="flex gap-5 justify-between items-center">
    <h2 id="search-heading" class="font-bold">Operadoras de plano de saúde ativas</h2>
    <div class="flex gap-4 text-sm">
      <div>
        <label for="category-select">Categoria: </label>
        <select
          name="category-select"
          id="category-select"
          :value="props.searchParams.category"
          @input="updateCategory(($event.target as HTMLSelectElement).value)"
          class="border-2 border-gray-600 rounded-sm px-px h-7"
          aria-label="Selecione a categoria de pesquisa"
        >
          <option
            v-for="category in SEARCH_CATEGORIES"
            :key="category.value"
            :value="category.value"
          >
            {{ category.label }}
          </option>
        </select>
      </div>
      <div>
        <label for="search-input">Pesquisar: </label>
        <input
          type="text"
          id="search-input"
          :value="props.searchParams.query"
          @input="updateQuery(($event.target as HTMLInputElement).value)"
          placeholder="administradora..."
          class="border-2 border-gray-600 rounded-sm px-px h-7"
          aria-label="Digite o termo de pesquisa"
        />
      </div>
    </div>
  </form>
</template>
