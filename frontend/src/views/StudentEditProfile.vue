<template>
    <Navbar role="student"/>

<div class="container mt-5">

    <div v-if="success">
        <h2 class="text-center mb-4">
            Edit Profile
        </h2>

        <form @submit.prevent="updateProfile">

            <div class="mb-3">

                <label class="form-label">Name</label>

                <input class="form-control" v-model="profile.name" disabled>

            </div>

            <div class="mb-3">

                <label class="form-label">Email</label>

                <input class="form-control" v-model="profile.email" disabled>

            </div>

            <div class="mb-3">

                <label class="form-label">Phone</label>

                <input class="form-control" v-model="profile.phone">

            </div>

            <div class="mb-3">

                <label class="form-label">Branch</label>

                <input class="form-control" v-model="profile.branch" disabled>

            </div>

            <div class="mb-3">

                <label class="form-label">Year</label>

                <input class="form-control" v-model="profile.year" disabled>

            </div>

            <div class="mb-3">

                <label class="form-label">CGPA</label>

                <input class="form-control" v-model="profile.cgpa" disabled>

            </div>

            <div class="mb-3">

                <label class="form-label">Skills</label>

                <textarea class="form-control" v-model="profile.skills"></textarea>

            </div>

            <div class="mb-3">

                <label class="form-label">LinkedIn</label>

                <input class="form-control" v-model="profile.linkedin">

            </div>

            <div class="mb-3">

                <label class="form-label">GitHub</label>

                <input class="form-control" v-model="profile.github">

            </div>

            <div class="mb-4">

                <label class="form-label">

                    Upload Resume

                </label>

                <input
                    type="file"
                    class="form-control"
                    @change="selectResume"
                >

            </div>

            <button class="btn btn-success">

                Save Changes

            </button>

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

            profile:{},

            resume:null

        }

    },

    components:{
        Navbar,
    },

    mounted(){

        this.loadProfile()

    },

    methods:{

        async loadProfile(){
            const response=await fetch(
                "http://127.0.0.1:5000/api/student/profile",
                {
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )
            const result=await response.json()
            if (result.success) {
                this.profile = result.profile
                if (!this.profile.is_active) {
                    this.success = false
                    this.message = "Inactive students cannot edit their profile."
                    return
                }
                if (this.profile.is_placed) {
                    this.success = false
                    this.message = "Placed students cannot edit their profile."
                    return
                }
                this.success = true
            }
            else {
                this.message = result.message
            }
        },


        selectResume(event){
            this.resume=event.target.files[0]
        },

        async updateProfile(){
            const formData=new FormData()
            formData.append("phone",this.profile.phone)
            formData.append("skills",this.profile.skills)
            formData.append("linkedin",this.profile.linkedin)
            formData.append("github",this.profile.github)
            if(this.resume){
                formData.append("resume",this.resume)
            }

            const response=await fetch(
                "http://127.0.0.1:5000/api/student/profile",
                {
                    method:"PUT",
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    },
                    body:formData
                }
            )
            const result=await response.json()
            alert(result.message)
            if(result.success){
                this.$router.push("/student/profile")
            }
        }
    }
}

</script>