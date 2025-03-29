<script setup lang="ts"></script>

<template>
  <main class="flex flex-col gap-6 border-2 border-gray-300 rounded-lg p-4">
    <section>
      <form v-on:submit.prevent class="flex gap-5 justify-between items-center">
        <legend class="font-bold">Operadoras de plano de saude ativas</legend>
        <div class="flex gap-4 text-sm">
          <div>
            <label for="category-select">Categoria: </label>
            <select
              name="category-select"
              id="category-select"
              class="border-2 border-gray-600 rounded-sm px-px h-7"
            >
              <option value="">Razão Social</option>
              <option value="">Nome Fantasia</option>
              <option value="">Modalidade</option>
            </select>
          </div>
          <div>
            <label for="search-input">Pesquisar: </label>
            <input
              type="text"
              id="search-input"
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
          <tr class="flex text-sm gap-12 border-b-1 border-gray-300">
            <th class="font-light">Registro ANS</th>
            <th class="font-light">Razão Social</th>
            <th class="font-light">Nome Fantasia</th>
            <th class="font-light">Modalidade</th>
            <th class="font-light">Cidade</th>
            <th class="font-light">Data de Registro ANS</th>
          </tr>
        </thead>
        <tbody>
          <tr></tr>
        </tbody>
      </table>
      <div class="text-center py-3">
        <h3>Digite na barra de pesquisas para obter resultados.</h3>
      </div>
    </section>
  </main>
</template>
