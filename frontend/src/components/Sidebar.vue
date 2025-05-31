<template>
  <aside class="">
    <div
      class="flex relative flex-col items-center w-64 h-full overflow-hidden text-gray-700 bg-gray-100 rounded shadow-lg shadow-[#c9c9c9]"
    >
      <div class="flex justify-center items-center w-full px-3 mt-4">
        <img class="w-12 h-12" src="@/img/logo.png" />
        <div class="flex flex-col justify-start mt-4 ml-2 text-[black]">
          <p class="text-5xl leading-[0.5] font-stengazeta">Тестовик</p>
          <p class="text-[15px] font-stengazeta">постановщик задач</p>
        </div>
      </div>
      <div class="w-full px-2">
        <div class="flex flex-col w-full mt-3 border-t border-gray-300">
          <router-link
            v-for="service in services"
            :key="service.name"
            :to="service.route"
          >
            <SidebarCategory
              :category="service.category"
              :name="service.name"
              :classed="service.classed"
              :isActive="service.isActive"
              :collapsed="!sidebarStatus"
            />
          </router-link>
        </div>
      </div>
    </div>
  </aside>
</template>
<script>
import SidebarCategory from "./SidebarCategory.vue";
import { mapGetters } from "vuex";
export default {
  components: {
    SidebarCategory,
  },
  data() {},
  computed: {
    services() {
      return [
        {
          category: "Главная",
          name: "laptop",
          classed: "w-8 h-8 ml-1",
          route: "/",
          isActive: this.$route.path === "/",
        },
      ];
    },
    ...mapGetters(["statementNumber"]),
  },
};
</script>
