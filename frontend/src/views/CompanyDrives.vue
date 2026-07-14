<template>
    <Navbar role="company"/>
    
    <div class="container mt-5">

        <div v-if="success">
        <h2 class="text-center mb-4">
            My Placement Drives
        </h2>

            <div class="card p-4 mb-5">
                <h4 class="mb-3">
                    Create New Drive
                </h4>

                <form @submit.prevent="createDrive">
                    <div class="mb-3">
                        <label class="form-label">Job Title</label>
                        <input type="text" class="form-control" v-model="job_title" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Specialization</label>
                        <input type="text" class="form-control" v-model="specialization" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Description</label>
                        <textarea class="form-control" v-model="description"></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">
                            Eligible Branches
                        </label>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="CSE" v-model="eligible_branches">
                            <label class="form-check-label">CSE</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="Data Science" v-model="eligible_branches">
                            <label class="form-check-label">Data Science</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="AI & ML" v-model="eligible_branches">
                            <label class="form-check-label">AI & ML</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="IT" v-model="eligible_branches">
                            <label class="form-check-label">IT</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="ECE" v-model="eligible_branches">
                            <label class="form-check-label">ECE</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="EEE" v-model="eligible_branches">
                            <label class="form-check-label">EEE</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="Mechanical" v-model="eligible_branches">
                            <label class="form-check-label">Mechanical</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="Civil" v-model="eligible_branches">
                            <label class="form-check-label">Civil</label>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Eligible Year</label>
                        <select class="form-select" v-model="eligible_year" required>
                            <option disabled value="">
                                Select Year
                            </option>
                            <option :value="1">1</option>
                            <option :value="2">2</option>
                            <option :value="3">3</option>
                            <option :value="4">4</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Minimum CGPA</label>
                        <input type="number" class="form-control" v-model="minimum_cgpa" min="0" max="10" step="0.01" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Application Deadline</label>
                        <input type="date" class="form-control" v-model="deadline" :min="today" required>
                    </div>

                    <button class="btn btn-success" type="submit">
                        Create Drive
                    </button>
                </form>
            </div>

            <h4 class="mb-3">
                Existing Drives
            </h4>

            <table class="table table-bordered table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Job Title</th>
                        <th>Specialization</th>
                        <th>Deadline</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="drive in drives" :key="drive.id">
                        <td>{{ drive.id }}</td>
                        <td>{{ drive.job_title }}</td>
                        <td>{{ drive.specialization }}</td>
                        <td>{{ drive.deadline }}</td>
                        <td>{{ drive.status }}</td>
                        <td>
                            <router-link v-if="drive.status=='Pending'" class="btn btn-warning btn-sm me-2" :to="'/company/drive/edit/'+drive.id">
                                Edit
                            </router-link>
                            <button v-if="drive.status=='Pending'" class="btn btn-danger btn-sm" @click="deleteDrive(drive.id)">
                                Delete
                            </button>
                            <router-link v-if="drive.status=='Approved' || drive.status=='Closed'" class="btn btn-primary btn-sm me-2" 
                                :to="'/company/drive/'+drive.id+'/applicants'">
                                View Applicants
                            </router-link>
                            <button v-if="drive.status=='Approved'" class="btn btn-warning btn-sm" @click="closeDrive(drive.id)">
                                Close
                            </button>
                            <button v-if="drive.status=='Rejected'" class="btn btn-danger btn-sm" @click="deleteDrive(drive.id)">
                                Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else>
            <div class="alert alert-danger text-center">
                {{ message }}
            </div>
        </div>

    </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"

export default {

    data() {
        return {
            success: false,
            message: "",
            today: new Date().toISOString().split("T")[0],
            drives: [],
            job_title: "",
            specialization: "",
            description: "",
            eligible_branches: [],
            eligible_year: "",
            minimum_cgpa: "",
            deadline: ""
        }
    },

    components:{
        Navbar,
    },

    mounted() {
        this.loadDrives()
    },

    methods: {

        async loadDrives() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/company/drives",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.success = true
                this.drives = result.drives
            }
            else {
                this.success = false
                this.message = result.message
            }
        },

        async createDrive() {
            if (this.eligible_branches.length == 0) {
                alert("Select at least one eligible branch")
                return
            }

            if (this.deadline < this.today) {
                alert("Deadline cannot be in the past")
                return
            }

            const response = await fetch(
                "http://127.0.0.1:5000/api/company/drives",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    },

                    body: JSON.stringify({
                        job_title: this.job_title,
                        specialization: this.specialization,
                        description: this.description,
                        eligible_branches: this.eligible_branches,
                        eligible_year: this.eligible_year,
                        minimum_cgpa: this.minimum_cgpa,
                        deadline: this.deadline
                    })
                }
            )

            const result = await response.json()
            alert(result.message)
            if (result.success) {
                this.job_title = ""
                this.specialization = ""
                this.description = ""
                this.eligible_branches = []
                this.eligible_year = ""
                this.minimum_cgpa = ""
                this.deadline = ""

                this.loadDrives()
            }
        },

        async deleteDrive(id) {
            if (!confirm("Delete this drive?")) {
                return
            }
            const response = await fetch(
                "http://127.0.0.1:5000/api/company/drive/"+id,
                {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            alert(result.message)
            this.loadDrives()  
        },

        async closeDrive(id) {
            if (!confirm("Close this drive?")) {
                return
            }

            const response = await fetch(
                "http://127.0.0.1:5000/api/company/drive/close/" + id,
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
        }
    }
}

</script>