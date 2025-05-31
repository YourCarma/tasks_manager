<template>
  <div class="h-full w-full p-2">
    <BaseAlert :color="'red'" :title="response_status" :text="response_detail" :state="isError"
      class="fixed top-4 right-4 z-50" />
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
          Создание задачи...
        </p>
      </div>
      <div v-else class="h-full w-full flex flex-col">
        <form @submit.prevent="create_task">
          <p class="text-2xl text-center w-full font-stengazeta px-4 py-4">
            <span class="text-3xl">Создание задачи </span>
          </p>
          <div class="w-full">
            <div>
              <p class="font-bold text-xl px-2 pt-2">Данные задачи</p>
            </div>
            <div class="w-full">
              <div class="w-full px-4 md:px-64">
                <div class="flex flex-col space-y-4">
                  <label class="block w-full">
                    <span class="block text-sm font-medium text-gray-700">Название</span>
                    <div class="relative mt-1">
                      <input v-model="this.task_name" type="text" :class="[
                        'block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                        'pr-24 md:pr-10',
                        this.errors.task_name
                          ? 'border-red-500 focus:border-red-500'
                          : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                      ]" />
                      <div class="hidden md:flex absolute inset-y-0 right-3 items-center space-x-2">
                        <span class="text-sm font-medium text-gray-700">Задача выполнена</span>
                        <input type="checkbox" v-model="this.task_completed"
                          class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500" />
                      </div>
                    </div>
                    <div class="mt-2 flex items-center space-x-2 md:hidden">
                      <input type="checkbox" checked
                        class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500" />
                      <span class="text-sm font-medium text-gray-700">Задача выполнена</span>
                    </div>
                  </label>
                  <div class="flex justify-end">
                    <button type="submit"
                      class="text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-8 py-2.5 focus:outline-none">
                      Создать задачу
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div>
            <p class="font-bold text-xl px-2 pt-2">Список текущих задач</p>
            <Tasks :tasks="tasks" @task-removed="onTaskRemoved" />
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import BaseAlert from "../components/BaseAlert.vue"
import Tasks from '../components/Tasks.vue';
export default {
  components: {
    BaseAlert,
    Tasks
  },

  data() {
    return {
      task_name: "Выполнить тестовое задание",
      tasks: [],
      task_completed: false,
      isServiceLoading: false,
      errors: {},
      activeIndex: 0,
      response_detail: 'Пусто',
      response_status: 'Пусто',
      isSending: false,
      isError: false
    };
  },
  async mounted() {
    try {
      const response = await axios.get(
        `http://${process.env.VUE_APP_MANAGER_SERVICE_HOST}:${process.env.VUE_APP_MANAGER_SERVICE_PORT}/api/tasks`,
      );
      this.tasks = response.data;
      console.info(this.tasks)

    }
    catch (error) {
      console.error("Error sending data:", error);
      this.isSending = false;
      this.isError = true;
      if (error.response) {
        this.response_detail = error.response.detail;
        this.response_status = error.response.status;
      }
      else {
        this.response_detail = "Сервис недоступен!"
        this.response_status = 503
      }
      this.isError = true;
      setTimeout(() => {
        this.isError = false;
      }, 4000);

    }
    this.isServiceLoading = true;
    setTimeout(() => {
      this.isServiceLoading = false;
    }, 1000);
  },

  methods: {
    onTaskRemoved(taskId) {
      this.tasks = this.tasks.filter(t => t.id !== taskId);
    },
    async create_task() {
      try {
        this.isSending = true;
        const response = await axios.post(
          `http://${process.env.VUE_APP_MANAGER_SERVICE_HOST}:${process.env.VUE_APP_MANAGER_SERVICE_PORT}/api/tasks`,
          {
            title: this.task_name,
            completed: this.task_completed,
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
        this.tasks.push(response.data);
      } catch (error) {
        console.error("Error sending data:", error);
        this.isSending = false;
        this.isError = true;
        if (error.response) {
          this.response_detail = error.response.data.detail;
          this.response_status = error.response.status;
        }
        else {
          this.response_detail = "Сервис недоступен!"
          this.response_status = 503
        }
        this.isError = true;
        setTimeout(() => {
          this.isError = false;
        }, 4000);

      }
    },
    setActive(index) {
      this.activeIndex = index;
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
