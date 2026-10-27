<template>
  <Dialog v-model:open="show" :size="'sm'" bare>
    <template #default>
      <div class="p-6">
        <div class="flex justify-center">
          <div class="flex flex-col items-center">
            <CRMLogo class="mb-3 size-12" />
            <Dialog.Title as-child>
              <h3 class="text-2xl-semibold text-ink-gray-9">PC CRM</h3>
            </Dialog.Title>
            <p class="text-sm text-ink-gray-6 mt-1">
              {{ __('Customer Relationship Management') }}
            </p>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>
<script setup>
import CRMLogo from '@/components/Icons/CRMLogo.vue'
import { Dialog } from 'frappe-ui'

let show = defineModel({ type: Boolean })
</script>

