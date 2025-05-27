<template>
  <div class="h-full w-full p-2">
    
    <div
      class="outline-1 outline shadow-[0_0px_5px_2px_rgba(0,0,0,0.1)] rounded-[5px] h-full flex flex-col flex-grow overflow-y-auto">
      <div v-if="this.isServiceLoading" class="h-full w-full flex flex-col justify-center items-center">
        <span class="loader"></span>
        <p class="text-black pt-2 font-stengazeta text-sm">
          Идет загрузка формы...
        </p>
      </div>
      <div v-else-if="this.isSending" class="h-full w-full flex flex-col justify-center items-center">
        <span class="loader"></span>
        <p class="text-black pt-2 font-stengazeta text-sm">
          Происходит анализ...
        </p>
      </div>
      <div v-else class="h-full w-full flex flex-col">
        <form @submit.prevent="handleSubmit">
          <p class="text-2xl text-center w-full font-stengazeta px-4 py-4">
            <span class="text-3xl">Создание жалобы </span>
          </p>
          <div class="w-full">
            <div>
              <p class="font-bold text-xl px-2 pt-2">Информация о заявителе</p>
            </div>
            <div class="w-full p-2 flex gap-4">
              <label class="block w-1/2">
                <span class="block text-sm font-medium text-gray-700">Имя</span>
                <input v-model="this.clientName" type="text" :class="[
                  'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                  this.errors.clientName
                    ? 'border-red-500 focus:border-red-500'
                    : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                ]" />
             
              </label>
              <label class="block w-1/2">
                <span class="block text-sm font-medium text-gray-700">Фамилия</span>
                <input v-model="this.clientSurname" type="text" :class="[
                  'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                  this.errors.clientAddress
                    ? 'border-red-500 focus:border-red-500'
                    : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                ]" />
              
              </label>
            </div>
            <div>
              <label class="block w-full px-2 pt-1">
                <span class="block text-sm font-medium text-gray-700">Ваши жалобы на жизнь</span>
                <textarea v-model="this.clientDefects"
                  class="mt-1 block w-full px-3 min-h-28 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>
              </label>
            </div>
          </div>
          <div class="flex justify-end py-2">
            <button type="submit"
              class="text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-8 py-2.5 me-2 mb-2 focus:outline-none">
              Отправить на решение проблем!
            </button>
          </div>
          <div>
              <p class="font-bold text-xl px-2 pt-2">Статус отправки жалобы</p>
              <p class="font-bold text-sm px-1 pt-2">Подробности: {{ response_detail }}</p>
              <p class="font-bold text-sm px-1 pt-2">HTTP статус: {{ response_status }}</p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import BaseAlert from "@/components/BaseAlert.vue";

export default {
  components: {
    BaseAlert
  },

  data() {
    return {
      clientName: "Самсон",
      clientSurname: "Аннович",
      clientDefects: "Не кормят",

      isServiceLoading: false,
      errors: {},
      activeIndex: 0,
      response_detail: 'Пусто',
      response_status: 'Пусто',
      isSending: false,
    };
  },
  mounted() {
    this.isServiceLoading = true;
    setTimeout(() => {
      this.isServiceLoading = false;
    }, 1000);
  },

  methods: {
    handleFiles(event) {
      const files = Array.from(event.target.files);
      const newFiles = files.map((file) => ({
        url: URL.createObjectURL(file),
        file,
      }));

      this.fileArr = [...this.fileArr, ...newFiles];
    },
    async handleSubmit() {

      try {
        this.isSending = true;
        const response = await axios.post(
          `http://${process.env.VUE_APP_GATEWAY_HOST}:${process.env.VUE_APP_GATEWAY_PORT}/service_a/create_request`,
          {
            name: this.clientName,
            surname: this.clientSurname,
            reason: this.clientDefects
          },
          {
            headers: {
              accept: "application/json",
            },
          }
        )
        
        console.log("Response from server:", response.data);
        this.isSending = false;
        this.response_detail = response.data
        this.response_status = response.status
      } catch (error) {
        console.error("Error sending data:", error);
        this.isSending = false;
        this.response_detail = error.response.data.detail
        this.response_status = error.response.status
      }
    },
    setActive(index) {
      this.activeIndex = index;
    },
    onInput(event) {
      let inputValue = event.target.value.replace(/\D+/g, ""); // remove non-digit characters
      const formattedValue = this.formatPhoneNumber(inputValue);
      event.target.value = formattedValue;
    },
  },
};
</script>
<style scoped>
.loader {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: inline-block;
  border-top: 3px solid #000000;
  border-right: 3px solid transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
