<template>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 p-4">
        <div v-for="task in tasks" :key="task.id"
            class="bg-white shadow-md rounded-xl p-4 border flex flex-col justify-between">
            <input v-model="task.title" type="text"
                class="text-lg font-semibold text-gray-800 bg-transparent border-b border-gray-300 focus:outline-none focus:border-blue-500" disabled/>
            <label class="inline-flex items-center mt-3 space-x-2">
                <input type="checkbox" v-model="task.completed" class="form-checkbox h-4 w-4 text-green-600" disabled />
                <span class="text-sm text-gray-600">
                    {{ task.completed ? "Выполнено" : "Не выполнено" }}
                </span>
            </label>
            <button @click.prevent="removeTask(task.id)"
                class="mt-4 text-white bg-red-500 hover:bg-red-600 font-medium rounded-lg text-sm px-4 py-2 self-end">
                Удалить
            </button>
        </div>
    </div>

</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            tasks: []
        };
    },
    props: {
        tasks: {
            Object: Array,
            require: true,
        },

    },
    methods: {
        async saveTask(task) {
            try {
                await axios.put(`http://${process.env.VUE_APP_MANAGER_SERVICE_HOST}:${process.env.VUE_APP_MANAGER_SERVICE_PORT}/api/tasks/${task.id}`, {
                    title: task.title,
                    completed: task.completed,
                });
                console.log(`Задача ${task.id} сохранена`);
            } catch (error) {
                console.error('Ошибка при сохранении задачи:', error);
            }
        },
        async removeTask(taskId) {
            try {
                await axios.delete(`http://${process.env.VUE_APP_MANAGER_SERVICE_HOST}:${process.env.VUE_APP_MANAGER_SERVICE_PORT}/api/tasks/${taskId}`);
                this.$emit('task-removed', taskId);
                console.log(`Задача ${taskId} удалена`);
            } catch (error) {
                console.error('Ошибка при удалении задачи:', error);
            }
        }
    }
}
</script>

<style scoped></style>