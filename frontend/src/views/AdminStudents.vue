<template>
    <Navbar role="admin"/>
    
    <div class="container mt-5">

        <h2 class="text-center mb-4">
            Manage Students
        </h2>

        <input type="text" class="form-control mb-4" placeholder="Search student by name/contact" v-model="searchText">

        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Contact</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="student in filteredStudents" :key="student.id">
                    <td>{{ student.id }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.phone }}</td>
                    <td>
                        <span v-if="student.blacklist_status">
                            Blacklisted
                        </span>
                        <span v-else-if="!student.is_active">
                            Inactive
                        </span>
                        <span v-else>
                            Active
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-primary btn-sm me-2" @click="viewStudent(student.id)">
                            View
                        </button>
                        <button v-if="!student.blacklist_status" class="btn btn-warning btn-sm me-2" @click="toggleActive(student.id)">
                            <span v-if="student.is_active">
                                Deactivate
                            </span>
                            <span v-else>
                                Activate
                            </span>
                        </button>
                        <button class="btn btn-danger btn-sm" @click="toggleBlacklist(student.id)">
                            <span>
                                Blacklist_Toggle
                            </span>
                        </button>
                    </td>
                </tr>
            </tbody>

        </table>
    </div>
</template>


<script>
import Navbar from "../components/Navbar.vue"

export default {

    data() {
        return {
            students: [],
            searchText: ""
        }
    },

    components:{
        Navbar,
    },

    computed: {
        filteredStudents() {
            return this.students.filter(student =>
                student.name.toLowerCase().includes(this.searchText.toLowerCase())
                ||
                student.phone.includes(this.searchText)
            )
        }
    },

    mounted() {
        this.loadStudents()
    },

    methods: {

        async loadStudents() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/students",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.students = result.students
            }
        },

        async toggleActive(id) {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/student/toggle-active/" + id,
                {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            alert(result.message)
            this.loadStudents()
        },

        async toggleBlacklist(id) {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/student/toggle-blacklist/" + id,
                {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            alert(result.message)
            this.loadStudents()
        },

        viewStudent(id) {
            this.$router.push("/admin/student/" + id)
        }
    }
}

</script>