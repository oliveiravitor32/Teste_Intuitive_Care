<script setup lang="ts">
import { useSearchService } from '@/composables/useSearchService'
const { searchParams, results, isEmpty, isLoading } = useSearchService()
</script>

<template>
  <main class="flex max-w-5xl flex-col gap-6 border-2 border-gray-300 rounded-lg p-4">
    <section>
      <form @submit.prevent class="flex gap-5 justify-between items-center">
        <fieldset>
          <legend class="font-bold">Operadoras de plano de saude ativas</legend>
        </fieldset>
        <div class="flex gap-4 text-sm">
          <div>
            <label for="category-select">Categoria: </label>
            <select
              name="category-select"
              id="category-select"
              v-model="searchParams.category"
              class="border-2 border-gray-600 rounded-sm px-px h-7"
            >
              <option value="razao_social">Razão Social</option>
              <option value="nome_fantasia">Nome Fantasia</option>
            </select>
          </div>
          <div>
            <label for="search-input">Pesquisar: </label>
            <input
              type="text"
              id="search-input"
              v-model="searchParams.query"
              placeholder="administradora..."
              class="border-2 border-gray-600 rounded-sm px-px h-7"
            />
          </div>
        </div>
      </form>
    </section>
    <section>
      <table>
        <thead>
          <tr class="grid grid-cols-6 text-sm border-b-1 border-gray-300">
            <th class="font-light">Registro ANS</th>
            <th class="font-light">Razão Social</th>
            <th class="font-light">Nome Fantasia</th>
            <th class="font-light">Modalidade</th>
            <th class="font-light">Cidade</th>
            <th class="font-light">Data de Registro ANS</th>
          </tr>
        </thead>

        <tbody>
          <tr
            class="hover:cursor-pointer py-2 text-center items-center text-xs hover:bg-neutral-300 grid grid-cols-6 gap-2 border-b-1 border-gray-300"
            v-for="(item, index) in results"
            :key="index"
          >
            <td>{{ item.registro_ans }}</td>
            <td>{{ item.razao_social.toLowerCase() }}</td>
            <td>{{ item.nome_fantasia?.toLowerCase() || '-' }}</td>
            <td>{{ item.modalidade?.toLowerCase() || '-' }}</td>
            <td>{{ item.cidade?.toLowerCase() || '-' }}</td>
            <td>{{ item.data_registro_ans?.toLowerCase() || '-' }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="isEmpty" class="text-center py-3">
        <h3>Digite na barra de pesquisas para obter resultados</h3>
      </div>
      <div v-if="isLoading" class="text-center py-3">
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      </div>
    </section>
  </main>
</template>
