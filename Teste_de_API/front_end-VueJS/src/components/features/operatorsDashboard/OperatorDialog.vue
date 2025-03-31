<script setup lang="ts">
import { operatorFieldDefinitions } from '@/constants/operator-field-definitions'
import type { IOperator } from '@/interfaces/operator.interface'
import { Button, Dialog } from 'primevue'
import { computed } from 'vue'

const props = defineProps<{
  selectedOperator: IOperator | null
  showDialog: boolean
}>()

const emit = defineEmits<{
  'update:showDialog': [boolean]
}>()

const updateVisibility = () => {
  emit('update:showDialog', false)
}

const formattedOperator = computed(() => {
  return operatorFieldDefinitions.reduce(
    (result, field) => {
      const value = props.selectedOperator?.[field.key as keyof IOperator]
      result[field.key] = field.formatter(value)
      return result
    },
    {} as Record<string, string>,
  )
})
</script>
<template>
  <Dialog
    :visible="props.showDialog"
    @update:visible="updateVisibility"
    modal
    header="Visualizando Operadora"
    :style="{ width: '100vw', maxWidth: '1024px' }"
    :content-class="'mx-4'"
  >
    <div class="p-2 rounded-sm">
      <span class="text-surface-500 text-center font-lg font-bold dark:text-surface-400 block mb-6"
        >Detalhes da Operadora</span
      >
      <dl class="w-full grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="(field, index) in operatorFieldDefinitions"
          :key="props.selectedOperator?.registro_ans || index"
          class="flex flex-col"
        >
          <dt class="text-gray-800 font-bold">{{ field.label }}:</dt>
          <dd class="text-sm">{{ formattedOperator[field.key] || '' }}</dd>
        </div>
      </dl>
      <div class="flex justify-center py-2">
        <Button type="button" label="Fechar" severity="danger" @click="updateVisibility"></Button>
      </div>
    </div>
  </Dialog>
</template>
