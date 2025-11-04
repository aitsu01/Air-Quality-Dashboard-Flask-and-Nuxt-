<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6 text-center">🌿 Stazioni di monitoraggio</h1>

    <div v-if="loading" class="text-center text-gray-600">Caricamento stazioni...</div>
    <div v-if="error" class="text-center text-red-600">{{ error }}</div>

    <!-- Lista stazioni -->
    <div
      v-if="stations.length"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"
    >
      <div
        v-for="station in stations"
        :key="station.id"
        @click="goToStation(station.id)"
        class="cursor-pointer p-5 border rounded-2xl shadow-md hover:shadow-lg hover:scale-[1.02] transition bg-white"
      >
        <h2 class="text-xl font-semibold mb-1">{{ station.name }}</h2>
        <p class="text-sm text-gray-600">{{ station.site }}</p>
        <p class="text-sm text-gray-500">{{ station.address }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'  // ✅ Importa il router

const stations = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()              // ✅ Inizializza il router

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:5000/api/stations')
    const data = await res.json()
    stations.value = data
  } catch (err) {
    error.value = 'Errore nel caricamento delle stazioni.'
  } finally {
    loading.value = false
  }
})

function goToStation(id) {
  router.push(`/station/${id}`)         // ✅ Naviga al dettaglio
}
</script>

