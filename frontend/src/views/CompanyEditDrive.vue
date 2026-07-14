<template>
    <Navbar role="company"/>

    <div class="container mt-5">

        <h2 class="text-center mb-4">
            Edit Placement Drive
        </h2>


        <div v-if="success">

            <form @submit.prevent="updateDrive">

                <div class="mb-3">
                    <label class="form-label">Job Title</label>
                    <input type="text" class="form-control" v-model="drive.job_title" required>
                </div>


                <div class="mb-3">
                    <label class="form-label">Specialization</label>
                    <input type="text" class="form-control" v-model="drive.specialization" required>
                </div>


                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control" v-model="drive.description"></textarea>
                </div>


                <div class="mb-3">

                    <label class="form-label">
                        Eligible Branches
                    </label>

                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="CSE" v-model="drive.eligible_branches">
                        <label class="form-check-label">CSE</label>
                    </div>

                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="Data Science" v-model="drive.eligible_branches">
                        <label class="form-check-label">Data Science</label>
                    </div>

                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="AI & ML" v-model="drive.eligible_branches">
                        <label class="form-check-label">AI & ML</label>
                    </div>

                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="IT" v-model="drive.eligible_branches">
                        <label class="form-check-label">IT</label>
                    </div>

                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="ECE" v-model="drive.eligible_branches">
                        <label class="form-check-label">ECE</label>
                    </div>

                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="EEE" v-model="drive.eligible_branches">
                        <label class="form-check-label">EEE</label>
                    </div>

                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="Mechanical" v-model="drive.eligible_branches">
                        <label class="form-check-label">Mechanical</label>
                    </div>

                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="Civil" v-model="drive.eligible_branches">
                        <label class="form-check-label">Civil</label>
                    </div>

                </div>


                <div class="mb-3">
                    <label class="form-label">Eligible Year</label>

                    <select class="form-select" v-model="drive.eligible_year">

                        <option :value="1">1</option>
                        <option :value="2">2</option>
                        <option :value="3">3</option>
                        <option :value="4">4</option>

                    </select>

                </div>


                <div class="mb-3">
                    <label class="form-label">Minimum CGPA</label>
                    <input type="number" class="form-control" v-model="drive.minimum_cgpa" min="0" max="10" step="0.01">
                </div>


                <div class="mb-4">
                    <label class="form-label">Deadline</label>
                    <input type="date" class="form-control" v-model="drive.deadline" :min="today" required>
                </div>


                <button class="btn btn-success" type="submit">
                    Save Changes
                </button>

                <router-link class="btn btn-primary m-2" to="/company/drives">
                    Back
                </router-link>

            </form>

        </div>

        <div v-else>
            <div class="alert alert-danger">
                {{ message }}
            </div>
        </div>

    </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"

export default{

    data(){
        return{
            success:false,
            message:"",
            today:new Date().toISOString().split("T")[0],
            drive:{}
        }
    },

    components:{
        Navbar,
    },

    mounted(){
        this.loadDrive()
    },

    methods:{

        async loadDrive(){
            const response=await fetch(
                "http://127.0.0.1:5000/api/company/drive/"+this.$route.params.id,
                {
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )

            const result=await response.json()
            if(result.success){
                this.success=true
                this.drive=result.drive
                this.drive.eligible_branches=this.drive.eligible_branches.split(",")
            }

            else{
                this.message=result.message
            }
        },

        async updateDrive(){
            if(this.drive.deadline<this.today){
                alert("Deadline cannot be in the past")
                return
            }

            const response=await fetch(
                "http://127.0.0.1:5000/api/company/drive/"+this.$route.params.id,
                {
                    method:"PUT",
                    headers:{
                        "Content-Type":"application/json",
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    },
                    body:JSON.stringify(this.drive)
                }
            )

            const result=await response.json()
            alert(result.message)
            if(result.success){
                this.$router.push("/company/drives")
            }
        }
    }
}

</script>