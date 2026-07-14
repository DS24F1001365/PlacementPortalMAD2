<template>
    <Navbar role="admin"/>
    <div class="container mt-5">

        <h2 class="text-center mb-4">
            Manage Placement Drives
        </h2>

        <input type="text" class="form-control mb-4" placeholder="Search by title/company" v-model="searchText">

        <table class="table table-bordered table-striped">

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Specialization</th>
                    <th>Company</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="drive in filteredDrives" :key="drive.id">
                    <td>{{ drive.id }}</td>
                    <td>{{ drive.title }}</td>
                    <td>{{ drive.specialization }}</td>
                    <td>{{ drive.company }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.status }}</td>
                    <td>
                        <button class="btn btn-primary btn-sm me-2" @click="viewDrive(drive.id)">
                            View
                        </button>
                        <button v-if="drive.status=='Pending'" class="btn btn-success btn-sm me-2" @click="approveDrive(drive.id)">
                            Approve
                        </button>
                        <button v-if="drive.status=='Pending'" class="btn btn-danger btn-sm" @click="rejectDrive(drive.id)">
                            Reject
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
            drives: [],
            searchText: ""
        }
    },

    components:{
        Navbar,
    },


    computed: {
        filteredDrives() {
            return this.drives.filter(drive =>
                drive.title.toLowerCase().includes(this.searchText.toLowerCase())
                ||
                drive.company.toLowerCase().includes(this.searchText.toLowerCase())
            )
        }
    },

    mounted() {
        this.loadDrives()
    },

    methods: {

        async loadDrives() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/drives",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.drives = result.drives
            }
        },

        async approveDrive(id) {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/drive/approve/" + id,
                {
                    method: "PUT",

                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            alert(result.message)
            this.loadDrives()
        },

        async rejectDrive(id) {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/drive/reject/" + id,
                {
                    method: "PUT",

                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            alert(result.message)
            this.loadDrives()
        },

        viewDrive(id) {
            this.$router.push("/admin/drive/" + id)
        }
    }
 }

</script>