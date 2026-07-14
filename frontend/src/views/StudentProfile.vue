<template>
    <Navbar role="student"/>
<div class="container mt-5">

    <div v-if="success">

        <h2 class="text-center mb-4">
            Student Profile
        </h2>

        <div class="card p-4">

            <p><b>Name:</b> {{ profile.name }}</p>

            <p><b>Email:</b> {{ profile.email }}</p>

            <p><b>Phone:</b> {{ profile.phone }}</p>

            <p><b>Branch:</b> {{ profile.branch }}</p>

            <p><b>Year:</b> {{ profile.year }}</p>

            <p><b>CGPA:</b> {{ profile.cgpa }}</p>

            <p><b>Skills:</b> {{ profile.skills }}</p>

            <p><b>LinkedIn:</b> {{ profile.linkedin }}</p>

            <p><b>GitHub:</b> {{ profile.github }}</p>

            <p>

                <b>Resume:</b>

                <a
                    v-if="profile.resume_path"
                    :href="'http://127.0.0.1:5000/uploads/resumes/' + profile.resume_path"
                    target="_blank"
                >
                    View Resume
                </a>

                <span v-else>
                    No Resume Uploaded
                </span>

            </p>

            <router-link
                v-if="profile.is_active && !profile.is_placed"
                class="btn btn-warning mt-3"
                to="/student/profile/edit">
                Edit Profile
            </router-link>

        </div>

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

            profile:{}

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

            if(result.success){

                this.success=true

                this.profile=result.profile

            }

            else{

                this.message=result.message

            }

        }

    }

}

</script>