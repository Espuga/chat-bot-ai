<script setup>
import AppMenu from './AppMenu.vue';
import AppTopbar from './AppTopbar.vue';



</script>

<template>
  <div class="flex flex-column h-screen">
    <!-- Topbar with fixed height -->
    <AppTopbar class="z-4" style="height: 60px;" />

    <!-- Main area below the topbar -->
    <div class="flex flex-row flex-1 overflow-hidden">
      <AppMenu class="col-2 h-full" />
      <div class="col-10 p-3 h-full overflow-hidden">
        <router-view />
      </div>
    </div>
  </div>
</template>