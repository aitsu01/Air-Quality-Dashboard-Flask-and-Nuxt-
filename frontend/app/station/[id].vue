<template>
  <div class="p-6">
    <button @click="$router.push('/')" class="text-blue-600 hover:underline mb-4">← Torna indietro</button>

    <div v-if="loading" class="text-center text-gray-600">Caricamento dati...</div>
    <div v-if="error" class="text-center text-red-600">{{ error }}</div>

    <div v-if="stationData" class="space-y-6">
      <h1 class="text-2xl font-bold">{{ stationData.name }}</h1>
      <p class="text-gray-500">{{ stationData.site }} – {{ stationData.address }}</p>

      <!-- Media ponderata -->
      <div class="bg-green-100 border-l-4 border-green-500 text-green-800 p-4 rounded">
        <p class="font-semibold">Medie ponderate (ultimi 7 giorni):</p>
        <ul class="list-disc list-inside">
          <li v-for="(value, key) in weightedAverages" :key="key">
            {{ key }}: {{ value ? value.toFixed(2) : 'n/d' }}
          </li>
        </ul>
      </div>

      <!-- Tabella -->
      <div v-for="(metric, key) in stationData.metrics" :key="key" class="overflow-x-auto">
        <h2 class="text-xl font-semibold mt-6 mb-2">{{ key }}</h2>
        <table class="min-w-full border border-gray-300 rounded-lg text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="border p-2">Giorno</th>
              <th class="border p-2">Min</th>
              <th class="border p-2">Media</th>
              <th class="border p-2">Max</th>
              <th class="border p-2">Sample Size</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(day, index) in metric" :key="index">
              <td class="border p-2">{{ day.date }}</td>
              <td class="border p-2">{{ day.min }}</td>
              <td class="border p-2">{{ day.average }}</td>
              <td class="border p-2">{{ day.max }}</td>
              <td class="border p-2">{{ day.sample_size }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const stationId = route.params.id
const stationData = ref(null)
const weightedAverages = ref({})
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/stations/${stationId}`)
    const data = await res.json()
    if (data.error) throw new Error(data.error)

    stationData.value = data

    // estrai le medie ponderate
    for (const [key, val] of Object.entries(data.metrics)) {
      if (key.endsWith('_weighted_avg')) {
        weightedAverages.value[key.replace('_weighted_avg', '')] = val
      }
    }
  } catch (err) {
    error.value = 'Errore nel caricamento della stazione.'
  } finally {
    loading.value = false
  }
})
</script>

